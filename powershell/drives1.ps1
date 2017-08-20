function getinfo
{
	[cmdletbinding()]
	param ($computername)
	get-wmiobject -class win32_computersystem -computername $computername
}

getinfo