# terraform/main.tf
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 4.0"
    }
  }
}

provider "google" {
  project = "smarter-home-demo"
  region  = "us-central1"
}

resource "google_service_account" "my_service_account" {
  account_id   = "smarter-home-service-account"
  display_name = "Smarter Home Service Account"
}

resource "google_project_iam_member" "storage_access" {
  project = "smarter-home-demo"
  role    = "roles/storage.objectViewer"
  member  = "serviceAccount:${google_service_account.my_service_account.email}"
}


# Create a VPC network
resource "google_compute_network" "vpc" {
  name                    = "my-network"
  auto_create_subnetworks = false
}

resource "google_compute_address" "static_ip" {
  name   = "iot-server-static-ip"
  region = "us-central1"  # Change to your instance's region
}

# Create a subnet
resource "google_compute_subnetwork" "subnet" {
  name          = "my-subnet"
  ip_cidr_range = "10.0.10.0/24"
  network       = google_compute_network.vpc.id
  region        = "us-central1"
}

# VM instance
resource "google_compute_instance" "vm" {
  name         = "iot-server-free-tier-instance"
  machine_type = "e2-micro"
  zone         = "us-central1-a"

  boot_disk {
    initialize_params {
      image = "ubuntu-os-cloud/ubuntu-2204-lts"
      size  = 10  # Stay within free tier
    }
  }

  network_interface {
    network    = google_compute_network.vpc.name
    subnetwork = google_compute_subnetwork.subnet.name
    access_config {
      nat_ip = google_compute_address.static_ip.address
      // Ephemeral public IP
    }
  }

  metadata = {
    startup-script = file("${path.module}/startup.sh")
  }

  service_account {
    email  = google_service_account.my_service_account.email
    scopes = ["https://www.googleapis.com/auth/cloud-platform"]
  }

  # Allow required traffic
  tags = ["wireguard", "ssh"]
}

# Firewall rules
resource "google_compute_firewall" "wireguard" {
  name    = "allow-wireguard"
  network = google_compute_network.vpc.name

  allow {
    protocol = "udp"
    ports    = ["51820"]  # WireGuard port
  }

  source_ranges = ["0.0.0.0/0"]
  target_tags   = ["wireguard"]
}

resource "google_compute_firewall" "ssh" {
  name    = "allow-internal-ssh"
  network = google_compute_network.vpc.name

  allow {
    protocol = "tcp"
    ports    = ["22"]  # WireGuard port
  }

  source_ranges = ["0.0.0.0/0"]
  target_tags   = ["ssh"]
}