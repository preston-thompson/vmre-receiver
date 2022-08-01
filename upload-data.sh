#!/bin/bash

VMRE_PATH=$HOME/vmre-receiver
RSYNC_LOG=$VMRE_PATH/rsync.log
DATA_PATH=$VMRE_PATH/data
STATION_ID=1
DAYS_KEEP=90
DAYS_UPLOAD=30

# Log the date and time
date | tee $RSYNC_LOG

# Delete data files older than DAYS_KEEP
# (this keeps the station's drive from getting full)
find $DATA_PATH/ -mindepth 1 -mtime +$DAYS_KEEP -delete

# Upload data files newer than DAYS_UPLOAD
# (this keeps the server's drive from getting full)
rsync -av --files-from=<(find $DATA_PATH/ -mtime -$DAYS_UPLOAD -type f -exec basename {} \;) $DATA_PATH/ rvra@carpetandbricks.com:vmre/data/station$STATION_ID/ | tee $RSYNC_LOG

