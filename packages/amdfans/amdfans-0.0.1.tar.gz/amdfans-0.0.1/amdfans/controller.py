from .utilities import confirm_dir, confirm_file, NodeException
from ww import f as fstr
import getpass
import grp
import math
import os
import pwd

class Controller:
  @classmethod
  def main(self):
    percentage = ui.get('percentage')
    amd_dir = '/sys/class/drm'

    try:
      confirm_dir(amd_dir)
    except NodeException as e:
      logger.error(e)
      return

    for root, dirs, files in os.walk(amd_dir):
      for d in dirs:
        try:
          # Skip unrelated dirs
          if "-" in d or not "card" in d:
            continue

          # Confirm card and parent hwmon dirs
          card_path = os.path.join(root, d)
          confirm_dir(card_path)
          parent_hwmon = os.path.join(card_path, 'device/hwmon')
          confirm_dir(parent_hwmon)

          for hw_root, hw_dirs, hw_files in os.walk(parent_hwmon):
            for hw_d in hw_dirs:
              if not "hwmon" in hw_d:
                continue

              # Confirm child hwmon dir
              child_hwmon = os.path.join(hw_root, hw_d)
              confirm_dir(child_hwmon)

              # Confirm pwm1 files
              pwm1_max = os.path.join(child_hwmon, 'pwm1_max')
              confirm_file(pwm1_max)
              pwm1_enable = os.path.join(child_hwmon, 'pwm1_enable')
              confirm_file(pwm1_enable)
              pwm1 = os.path.join(child_hwmon, 'pwm1')
              confirm_file(pwm1)

              # Confirm pwm1_max file has contents
              try:
                with open(pwm1_max, 'r') as f:
                  pwm1_max_setting = int( f.readline() )
              except:
                logger.error( fstr("{d} has an empty pwm1_max file. Skipping.") )
                continue

              # Set GPU speed relative to pwm1_max_setting
              gpu_fan_speed = math.trunc( ( ( int(pwm1_max_setting) * int(percentage) ) / 100 ) )

              # Give current user ownership of pwm1 and pwm1_enable
              user = getpass.getuser()
              uid = pwd.getpwnam(user).pw_uid
              gid = grp.getgrnam(user).gr_gid
              os.chown(pwm1, uid, gid)
              os.chown(pwm1_enable, uid, gid)

              # Enable pwm1
              with open(pwm1_enable, 'w+') as f:
                f.write("1")
                f.close()

              # Set GPU fan speed
              with open(pwm1, 'w+') as f:
                f.write( str(gpu_fan_speed) )
                f.close()

              # Check settings for persistence
              pwm1_enable_setting = open(pwm1_enable, 'r').read()
              if "1" in pwm1_enable_setting:
                logger.info( fstr("{d} manual fan settings enabled") , color="green")
              else:
                logger.error( fstr("{d} manual fan settings could not be enabled") )

              with open(pwm1, 'r') as f:
                setting = int( f.readline() )
                setting_upper = setting + 15
                setting_lower = setting - 10

                if not gpu_fan_speed == setting:
                  if gpu_fan_speed < setting_lower:
                    logger.error( fstr("{d} fan speed setting failed") )
                    return
                  elif gpu_fan_speed > setting_upper:
                    logger.error( fstr("{d} fan speed setting may be too high") )
                    return
                  
                logger.info( fstr("{d} fan speed set to {percentage}%") , color="green")

        except NodeException as e:
          logger.error(e)
          continue

    return True