# WinSCP

## Edit config files with an editor on windows

### 1. **Connect with WinSCP as root (or with sudo)**
- **Best:** Use the `root` account for full access.
- **If you must use a non-root user:**  
  - Your user must have sudo privileges.
  - In WinSCP, go to **Advanced Site Settings → Environment → SFTP** and set **SFTP server** to:

    ```bash
    sudo /usr/lib/openssh/sftp-server
    ```

    or (on ubuntu 24):

    ```bash
    sudo /usr/lib/sftp-server 
    ```

