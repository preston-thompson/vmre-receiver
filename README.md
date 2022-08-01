# Linux setup

So that the VMRE receiver will run any time the PC is on, and to upload data automatically, enter into the crontab:
```
0 * * * * /path/to/vmre-receiver/upload-data.sh
*/5 * * * * /path/to/vmre-receiver/vmre-start.sh
```

Modify config.py.

# Windows setup

## Windows Task Scheduler

Create a task to run the upload script automatically. The trigger should be "Daily, At 2:00 AM every day" - "After triggered, repeat every 1 hour indefinitely.". The action should be "start a program" - the command should be:
```
"C:\Program Files (x86)\WinSCP\WinSCP.com" /script=C:\path\to\vmre-receiver\vmre-winscp-script.txt
```

## WinSCP script

Modify vmre-winscp-script.txt.

