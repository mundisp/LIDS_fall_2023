#!/usr/bin/env bash




# copy crontab to current_cron
crontab -l > current_cron

# remove lines between the two markers
sed '/---script managed section---/q' current_cron > new_cron

# add new cron jobs

cat >> new_cron << EOF

# DO NOT MODIFY THE SECTION BELOW MANUALLY.  IT'S MANAGED BY AUTOMATION.
#---script managed section---

@reboot bash /home/kali/CS4311_LIDS_2AllSafe_Fall2023/lnids_starter.sh
EOF

# add back the lines after the second marker
crontab < new_cron

# remove temp files
rm -f new_cron current_cron
