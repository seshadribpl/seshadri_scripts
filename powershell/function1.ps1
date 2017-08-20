function fileinfo 
{
    param($filename)
    # (cmdletbinding[])
    # $contents = get-content $filename
    # foreach ($name in $contents)
    # {
    #     $name
    # }
    get-content $filename
}
fileinfo -filename /etc/fstab 