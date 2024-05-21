#!/bin/bash
conf_start=11
conf_step=10
conf_end=999
basedir="ini"

for i in $(seq ${conf_start} ${conf_step} ${conf_end} ); do
  j=$(printf %04d $i)

  ccfg_dir="${base_dir}/cnfg${j}"
  
  if [ -d "${cfg_dir}" ]; then
    cd ${cfg_dir}
    
    echo "Starting config ${i}"
    perams="perams_${j}.sh"
    
    if [ -f "${perams}" ]; then
      sbatch ${perams}
    else
      echo "Shell script ${perams} not found in ${cfg_dir}"
    fi
    
    cd - > /dev/null
  else
    echo "Configuration directory ${cfg_dir} does not exist"
  fi
done