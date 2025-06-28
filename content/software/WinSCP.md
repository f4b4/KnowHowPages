# WinSCP

## Edit config files with an editor on windows

### 1. **Connect with WinSCP as root (or with sudo)**
- **Best:** Use the `root` account for full access.
- **If you must use a non-root user:**  
  - Your user must have sudo privileges.
  - In WinSCP, go to **Advanced Site Settings → Environment → SFTP** and set **SFTP server** to:

    ```
    sudo /usr/lib/openssh/sftp-server
    ```

    or (on some ubuntu 24):
    
    ```
    sudo /usr/lib/sftp-server 
    ```

