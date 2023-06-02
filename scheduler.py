from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

import scheduler.main

# scheduler.main.test_scheduler()
scheduler.main.scheduler_main()