#!/bin/bash -e

# script that sends mail if resources are low
subject="Server Resource Limits Alert"
from="project-liberation.monitor@codepoets.it"
to="admin-notifications@codepoets.it"

function check_free_space {
    disk_name="$1"
    local free_space="$(df | grep -w $disk_name | awk '{ print $4 }')"
    if [ -z "$free_space" ]; then
        echo "There is a problem with checking free space on disk. Please check if mount point \"$disk_name\" exist."
        exit 1
    fi
    # Convert kilobyte to megabyte
    let free_space=$free_space/1024
    echo $free_space
}

## Available free memory size in megabytes(MB)
available_memory="$(free -m | grep Mem | awk '{print $7}')"
if [[ "$available_memory" -le 100 ]]; then

    warning_message+="$(
	cat <<-END
		
		
		+------------------------------------------------------------------+\n
		Memory information\n\n
		Warning, server memory is running low!\n
		Free memory: $available_memory MB\n
		
		
		Top processes consuming memory resources:\n
		$(ps -eo pid,ppid,cmd,%mem,%cpu --sort=-%mem | head)\n
		+------------------------------------------------------------------+\n
	END
    )"

fi

cpu_usage="$(cat /proc/loadavg | awk '{print $1}')"
cpu_usage_converted_to_int=${cpu_usage%.*}
if [[ "$cpu_usage_converted_to_int" -ge 80 ]]; then
    warning_message+="$(
	cat <<-END
		
		
		+------------------------------------------------------------------+\n
		CPU information\n\n
		Warning, current cpu utilization is: $cpu_usage_converted_to_int %\n
		
		
		Top processes consuming cpu resources:\n
		$(ps -eo pid,ppid,cmd,%mem,%cpu --sort=-%cpu | head)\n
		+------------------------------------------------------------------+\n
	END
    )"
fi

disks=(
        /dev/sda1
        /dev/sdb
)

for disk in ${disks[@]}; do
    free_space_on_disk="$(check_free_space $disk)"
    if [[ "$free_space_on_disk" -le 2048 ]]; then

        warning_message+="$(
		cat <<-END
		
		
		+------------------------------------------------------------------+\n
		Disk space information\n\n
		Warning, the "$disk" partition has currently $free_space_on_disk MB of free space\n
		
		+------------------------------------------------------------------+\n
		END
        )"
    fi
done


if [ ! -z "$warning_message" ]; then
    echo -e "$warning_message" | mailx --subject "$subject" --return-address "$from" "$to"
fi
