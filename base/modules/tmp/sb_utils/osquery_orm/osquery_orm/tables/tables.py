from peewee import Database, Model
from . import cross_platform, freebsd, linux, macos, windows
from .platform_base import mac_lin, mac_lin_win, mac_win


class BindDatabase:
    def __init__(self, conn: Database):
        models = []
        for prop in dir(self):
            if not prop.startswith('_'):
                val = getattr(self, prop)
                if issubclass(val, Model):
                    models.append(val)
        conn.bind(models)


class CrossPlatform(BindDatabase):
    ARP_Cache = cross_platform.ArpCache
    AtomPackages = cross_platform.AtomPackages
    AzureInstanceMetadata = cross_platform.AzureInstanceMetadata
    AzureInstanceTags = cross_platform.AzureInstanceTags
    CarbonBlackInfo = cross_platform.CarbonBlackInfo
    Carves = cross_platform.Carves
    ChromeExtensionContentScripts = cross_platform.ChromeExtensionContentScripts
    ChromeExtensions = cross_platform.ChromeExtensions
    CPUID = cross_platform.Cpuid
    Curl = cross_platform.Curl
    CurlCertificate = cross_platform.CurlCertificate
    EC2_InstanceMetadata = cross_platform.Ec2InstanceMetadata
    EC2_InstanceTags = cross_platform.Ec2InstanceTags
    EtcHosts = cross_platform.EtcHosts
    EtcProtocols = cross_platform.EtcProtocols
    EtcServices = cross_platform.EtcServices
    # example
    File = cross_platform.File  # overwritten in MacOS, Linux, Windows
    FirefoxAddons = cross_platform.FirefoxAddons
    Groups = cross_platform.Groups  # overwritten in MacOS, Windows
    Hash = cross_platform.Hash  # overwritten in Linux
    IntelMeInfo = cross_platform.IntelMeInfo
    InterfaceAddresses = cross_platform.InterfaceAddresses  # overwritten in Windows
    InterfaceDetails = cross_platform.InterfaceDetails  # overwritten in Linux, Windows
    KernelInfo = cross_platform.KernelInfo
    ListeningPorts = cross_platform.ListeningPorts  # overwritten in Linux
    LoggedInUsers = cross_platform.LoggedInUsers  # overwritten in Windows
    OS_Version = cross_platform.OSVersion  # overwritten in Linux, Windows
    OsqueryEvents = cross_platform.OsqueryEvents
    OsqueryExtensions = cross_platform.OsqueryExtensions
    OsqueryFlags = cross_platform.OsqueryFlags
    OsqueryInfo = cross_platform.OsqueryInfo
    OsqueryPacks = cross_platform.OsqueryPacks
    OsqueryRegistry = cross_platform.OsqueryRegistry
    OsquerySchedule = cross_platform.OsquerySchedule
    PlatformInfo = cross_platform.PlatformInfo
    ProcessMemoryMap = cross_platform.ProcessMemoryMap
    ProcessOpenSockets = cross_platform.ProcessOpenSockets  # overwritten in MacOS, Linux, Windows
    Processes = cross_platform.Processes  # overwritten in MacOS, Windows
    PythonPackages = cross_platform.PythonPackages
    Routes = cross_platform.Routes
    SSH_Configs = cross_platform.SshConfigs
    StartupItems = cross_platform.StartupItems
    SystemInfo = cross_platform.SystemInfo
    Time = cross_platform.Time  # overwritten in Windows
    Uptime = cross_platform.Uptime
    UserGroups = cross_platform.UserGroups
    UserSSHKeys = cross_platform.UserSshKeys
    Users = cross_platform.Users  # overwritten in MacOS, Windows
    YcloudInstanceMetadata = cross_platform.YcloudInstanceMetadata
    # Posix_Hash
    # Posix_InterfaceDetails
    # Posix_Routes


class FreeBSD(CrossPlatform):
    FbsdKmods = freebsd.FbsdKmods
    PkgPackages = freebsd.PkgPackages


class MacOS_Linux(CrossPlatform):
    AcpiTables = mac_lin.AcpiTables
    AptSources = mac_lin.AptSources
    Augeas = mac_lin.Augeas
    AuthorizedKeys = mac_lin.AuthorizedKeys
    BlockDevices = mac_lin.BlockDevices
    CpuTime = mac_lin.CpuTime
    Crontab = mac_lin.Crontab
    DeviceFile = mac_lin.DeviceFile
    DeviceHash = mac_lin.DeviceHash
    DevicePartitions = mac_lin.DevicePartitions
    DiskEncryption = mac_lin.DiskEncryption  # overwritten in MacOS
    DnsResolvers = mac_lin.DnsResolvers
    DockerContainerFsChanges = mac_lin.DockerContainerFsChanges
    DockerContainerLabels = mac_lin.DockerContainerLabels
    DockerContainerMounts = mac_lin.DockerContainerMounts
    DockerContainerNetworks = mac_lin.DockerContainerNetworks
    DockerContainerPorts = mac_lin.DockerContainerPorts
    DockerContainerProcesses = mac_lin.DockerContainerProcesses
    DockerContainerStats = mac_lin.DockerContainerStats
    DockerContainers = mac_lin.DockerContainers  # overitten in Linux
    DockerImageHistory = mac_lin.DockerImageHistory
    DockerImageLabels = mac_lin.DockerImageLabels
    DockerImageLayers = mac_lin.DockerImageLayers
    DockerImages = mac_lin.DockerImages
    DockerInfo = mac_lin.DockerInfo
    DockerNetworkLabels = mac_lin.DockerNetworkLabels
    DockerNetworks = mac_lin.DockerNetworks
    DockerVersion = mac_lin.DockerVersion
    DockerVolumeLabels = mac_lin.DockerVolumeLabels
    DockerVolumes = mac_lin.DockerVolumes
    ExtendedAttributes = mac_lin.ExtendedAttributes
    FileEvents = mac_lin.FileEvents
    HardwareEvents = mac_lin.HardwareEvents
    InterfaceIpv6 = mac_lin.InterfaceIpv6
    KnownHosts = mac_lin.KnownHosts
    Last = mac_lin.Last
    LoadAverage = mac_lin.LoadAverage
    LxdCertificates = mac_lin.LxdCertificates
    LxdCluster = mac_lin.LxdCluster
    LxdClusterMembers = mac_lin.LxdClusterMembers
    LxdImages = mac_lin.LxdImages
    LxdInstanceConfig = mac_lin.LxdInstanceConfig
    LxdInstanceDevices = mac_lin.LxdInstanceDevices
    LxdInstances = mac_lin.LxdInstances
    LxdNetworks = mac_lin.LxdNetworks
    LxdStoragePools = mac_lin.LxdStoragePools
    Magic = mac_lin.Magic
    MemoryArrayMappedAddresses = mac_lin.MemoryArrayMappedAddresses
    MemoryArrays = mac_lin.MemoryArrays
    MemoryDeviceMappedAddresses = mac_lin.MemoryDeviceMappedAddresses
    MemoryDevices = mac_lin.MemoryDevices
    MemoryErrorInfo = mac_lin.MemoryErrorInfo
    Mounts = mac_lin.Mounts
    OemStrings = mac_lin.OemStrings
    PciDevices = mac_lin.PciDevices  # overwritten in Linux
    ProcessEnvs = mac_lin.ProcessEnvs
    ProcessOpenFiles = mac_lin.ProcessOpenFiles
    ProcessOpenPipes = mac_lin.ProcessOpenPipes
    ProcessEvents = mac_lin.ProcessEvents  # overwritten in MacOS, Linux
    PrometheusMetrics = mac_lin.PrometheusMetrics
    ShellHistory = mac_lin.ShellHistory
    SmartDriveInfo = mac_lin.SmartDriveInfo
    SmbiosTables = mac_lin.SmbiosTables
    SocketEvents = mac_lin.SocketEvents
    Sudoers = mac_lin.Sudoers
    SuidBin = mac_lin.SuidBin
    SystemControls = mac_lin.SystemControls  # overwritten in MacOS
    UlimitInfo = mac_lin.UlimitInfo
    UsbDevices = mac_lin.UsbDevices
    UserEvents = mac_lin.UserEvents
    YumSources = mac_lin.YumSources


class MacOS_Windows(CrossPlatform):
    Certificates = mac_win.Certificates  # overwritten in Windows


class MacOS_Linux_Windows(CrossPlatform):
    Yara = mac_lin_win.Yara
    YaraEvents = mac_lin_win.YaraEvents


class Linux(MacOS_Linux, MacOS_Linux_Windows):
    # acpi_tables
    ApparmorEvents = linux.ApparmorEvents
    ApparmorProfiles = linux.ApparmorProfiles
    # apt_sources
    # augeas
    # authorized_keys
    # block_devices
    BpfProcessEvents = linux.BpfProcessEvents
    BpfSocketEvents = linux.BpfSocketEvents
    # cpu_time
    # crontab
    DebPackages = linux.Linux_DebPackages  # DebPackages
    # device_file
    # device_hash
    # device_partitions
    # disk_encryption
    # dns_resolvers
    # docker_container_fs_changes
    # docker_container_labels
    # docker_container_mounts
    # docker_container_networks
    # docker_container_ports
    # docker_container_processes
    # docker_container_stats
    DockerContainers = mac_lin.Linux_DockerContainers
    # docker_image_history
    # docker_image_labels
    # docker_image_layers
    # docker_images
    # docker_info
    # docker_network_labels
    # docker_networks
    # docker_version
    # docker_volume_labels
    # docker_volumes
    ElfDynamic = linux.ElfDynamic
    ElfInfo = linux.ElfInfo
    ElfSections = linux.ElfSections
    ElfSegments = linux.ElfSegments
    ElfSymbols = linux.ElfSymbols
    # extended_attributes
    File = cross_platform.Linux_File
    # file_events
    # hardware_events
    Hash = cross_platform.Linux_Hash
    InterfaceDetails = cross_platform.Linux_InterfaceDetails
    # interface_ipv6
    IP_Tables = linux.Iptables
    KernelModules = linux.KernelModules
    # known_hosts
    # last
    ListeningPorts = cross_platform.Linux_ListeningPorts
    LldpNeighbors = linux.LldpNeighbors
    # load_average
    # lxd_certificates
    # lxd_cluster
    # lxd_cluster_members
    # lxd_images
    # lxd_instance_config
    # lxd_instance_devices
    # lxd_instances
    # lxd_networks
    # lxd_storage_pools
    # magic
    MdDevices = linux.MdDevices
    MdDrives = linux.MdDrives
    MdPersonalities = linux.MdPersonalities
    # memory_array_mapped_addresses
    # memory_arrays
    # memory_device_mapped_addresses
    # memory_devices
    # memory_error_info
    MemoryInfo = linux.MemoryInfo
    MemoryMap = linux.MemoryMap
    # mounts
    Msr = linux.Msr
    NpmPackages = linux.Linux_NpmPackages  # NpmPackages
    # oem_strings
    OS_Version = cross_platform.Linux_OSVersion
    PciDevices = mac_lin.Linux_PciDevices
    PortageKeywords = linux.PortageKeywords
    PortagePackages = linux.PortagePackages
    PortageUse = linux.PortageUse
    # process_envs
    ProcessEvents = mac_lin.Linux_ProcessEvents
    ProcessFileEvents = linux.ProcessFileEvents
    ProcessNamespaces = linux.ProcessNamespaces
    # process_open_files
    # process_open_pipes
    ProcessOpenSockets = cross_platform.Linux_ProcessOpenSockets
    # prometheus_metrics
    RpmPackageFiles = linux.RpmPackageFiles
    RpmPackages = linux.Linux_RpmPackages  # RpmPackages
    SeccompEvents = linux.SeccompEvents
    SelinuxEvents = linux.SelinuxEvents
    SelinuxSettings = linux.SelinuxSettings
    Shadow = linux.Shadow
    SharedMemory = linux.SharedMemory
    # shell_history
    # smart_drive_info
    # smbios_tables
    # socket_events
    # sudoers
    # suid_bin
    SyslogEvents = linux.SyslogEvents
    # system_controls
    # system_info
    SystemdUnits = linux.SystemdUnits
    # ulimit_info
    # usb_devices
    # user_events
    # yara
    # yara_events
    # yum_sources


class MacOS(MacOS_Linux, MacOS_Windows, MacOS_Linux_Windows):
    AccountPolicyData = macos.AccountPolicyData
    # acpi_tables
    AdConfig = macos.AdConfig
    Alf = macos.Alf
    AlfExceptions = macos.AlfExceptions
    AlfExplicitAuths = macos.AlfExplicitAuths
    AppSchemes = macos.AppSchemes
    Apps = macos.Apps
    # apt_sources
    Asl = macos.Asl
    # augeas
    AuthorizationMechanisms = macos.AuthorizationMechanisms
    Authorizations = macos.Authorizations
    # authorized_keys
    Battery = macos.Battery
    # block_devices
    BrowserPlugins = macos.BrowserPlugins
    # certificates
    # cpu_time
    Crashes = macos.Crashes
    # crontab
    CupsDestinations = macos.CupsDestinations
    CupsJobs = macos.CupsJobs
    # device_file
    DeviceFirmware = macos.DeviceFirmware
    # device_hash
    # device_partitions
    DiskEncryption = mac_lin.MacOS_DiskEncryption
    DiskEvents = macos.DiskEvents
    # dns_resolvers
    # docker_container_fs_changes
    # docker_container_labels
    # docker_container_mounts
    # docker_container_networks
    # docker_container_ports
    # docker_container_processes
    # docker_container_stats
    # docker_containers
    # docker_image_history
    # docker_image_labels
    # docker_image_layers
    # docker_images
    # docker_info
    # docker_network_labels
    # docker_networks
    # docker_version
    # docker_volume_labels
    # docker_volumes
    EsProcessEvents = macos.EsProcessEvents
    EventTaps = macos.EventTaps
    # extended_attributes
    FanSpeedSensors = macos.FanSpeedSensors
    File = cross_platform.MacOS_File
    # file_events
    Gatekeeper = macos.Gatekeeper
    GatekeeperApprovedApps = macos.GatekeeperApprovedApps
    Groups = cross_platform.MacOS_Groups
    # hardware_events
    HomebrewPackages = macos.HomebrewPackages
    IbridgeInfo = macos.IbridgeInfo
    # interface_ipv6
    IokitDevicetree = macos.IokitDevicetree
    IokitRegistry = macos.IokitRegistry
    KernelExtensions = macos.KernelExtensions
    KernelPanics = macos.KernelPanics
    KeychainAcls = macos.KeychainAcls
    KeychainItems = macos.KeychainItems
    # known_hosts
    # last
    Launchd = macos.Launchd
    LaunchdOverrides = macos.LaunchdOverrides
    # load_average
    LocationServices = macos.LocationServices
    # lxd_certificates
    # lxd_cluster
    # lxd_cluster_members
    # lxd_images
    # lxd_instance_config
    # lxd_instance_devices
    # lxd_instances
    # lxd_networks
    # lxd_storage_pools
    # magic
    ManagedPolicies = macos.ManagedPolicies
    Mdfind = macos.Mdfind
    Mdls = macos.Mdls
    # memory_array_mapped_addresses
    # memory_arrays
    # memory_device_mapped_addresses
    # memory_devices
    # memory_error_info
    # mounts
    NfsShares = macos.NfsShares
    Nvram = macos.Nvram
    # oem_strings
    PackageBom = macos.PackageBom
    PackageInstallHistory = macos.PackageInstallHistory
    PackageReceipts = macos.PackageReceipts
    # pci_devices
    Plist = macos.Plist
    PowerSensors = macos.PowerSensors
    Preferences = macos.Preferences
    # process_envs
    ProcessEvents = mac_lin.MacOS_ProcessEvents
    # process_open_files
    # process_open_pipes
    ProcessOpenSockets = cross_platform.Linux_MacOS_Windows_ProcessOpenSockets
    Processes = cross_platform.MacOS_Processes
    # prometheus_metrics
    QuicklookCache = macos.QuicklookCache
    RunningApps = macos.RunningApps
    SafariExtensions = macos.SafariExtensions
    Sandboxes = macos.Sandboxes
    ScreenLock = macos.Screenlock
    SharedFolders = macos.SharedFolders
    SharingPreferences = macos.SharingPreferences
    # shell_history
    Signature = macos.Signature
    SipConfig = macos.SipConfig
    # smart_drive_info
    # smbios_tables
    SmcKeys = macos.SmcKeys
    # socket_events
    # sudoers
    # suid_bin
    SystemControls = mac_lin.MacOS_SystemControls
    SystemExtensions = macos.SystemExtensions
    TemperatureSensors = macos.TemperatureSensors
    TimeMachineBackups = macos.TimeMachineBackups
    TimeMachineDestinations = macos.TimeMachineDestinations
    # ulimit_info
    # usb_devices
    # user_events
    UserInteractionEvents = macos.UserInteractionEvents
    Users = cross_platform.MacOS_Users
    VirtualMemoryInfo = macos.VirtualMemoryInfo
    WiFiNetworks = macos.WifiNetworks
    WiFiStatus = macos.WifiStatus
    WiFiSurvey = macos.WifiSurvey
    XprotectEntries = macos.XprotectEntries
    XprotectMeta = macos.XprotectMeta
    XprotectReports = macos.XprotectReports
    # yara
    # yara_events
    # yum_sources


class Windows(MacOS_Windows, MacOS_Linux_Windows):
    AppcompatShims = windows.AppcompatShims
    Authenticode = windows.Authenticode
    Autoexec = windows.Autoexec
    BackgroundActivitiesModerator = windows.BackgroundActivitiesModerator
    BitlockerInfo = windows.BitlockerInfo
    Certificates = mac_win.Windows_Certificates
    ChassisInfo = windows.ChassisInfo
    ChocolateyPackages = windows.ChocolateyPackages
    Connectivity = windows.Connectivity
    CPU_Info = windows.CpuInfo
    DefaultEnvironment = windows.DefaultEnvironment
    DiskInfo = windows.DiskInfo
    DNS_Cache = windows.DnsCache
    Drivers = windows.Drivers
    File = cross_platform.Windows_File
    Groups = cross_platform.Windows_Groups
    HvciStatus = windows.HvciStatus
    IE_Extensions = windows.IeExtensions
    InterfaceAddresses = cross_platform.Windows_InterfaceAddresses
    InterfaceDetails = cross_platform.Windows_InterfaceDetails
    KvaSpeculativeInfo = windows.KvaSpeculativeInfo
    LoggedInUsers = cross_platform.Windows_LoggedInUsers
    LogicalDrives = windows.LogicalDrives
    LogonSessions = windows.LogonSessions
    Ntdomains = windows.Ntdomains
    NTFS_ACL_Permissions = windows.NtfsAclPermissions
    NTFS_JournalEvents = windows.NtfsJournalEvents
    OfficeMru = windows.OfficeMru
    OS_Version = cross_platform.Windows_OSVersion
    Patches = windows.Patches
    PhysicalDiskPerformance = windows.PhysicalDiskPerformance
    Pipes = windows.Pipes
    PowershellEvents = windows.PowershellEvents
    Prefetch = windows.Prefetch
    ProcessOpenSockets = cross_platform.Linux_MacOS_Windows_ProcessOpenSockets
    Processes = cross_platform.Windows_Processes
    Programs = windows.Programs
    Registry = windows.Registry
    ScheduledTasks = windows.ScheduledTasks
    Services = windows.Services
    SharedResources = windows.SharedResources
    ShellBags = windows.Shellbags
    Shimcache = windows.Shimcache
    ShortcutFiles = windows.ShortcutFiles
    Time = cross_platform.Windows_Time
    UserAssist = windows.Userassist
    Users = cross_platform.Windows_Users
    VideoInfo = windows.VideoInfo
    WinBaseObj = windows.Winbaseobj
    WindowsCrashes = windows.WindowsCrashes
    WindowsEventLog = windows.WindowsEventlog
    WindowsEvents = windows.WindowsEvents
    WindowsOptionalFeatures = windows.WindowsOptionalFeatures
    WindowsSecurityCenter = windows.WindowsSecurityCenter
    WindowsSecurityProducts = windows.WindowsSecurityProducts
    WmiBiosInfo = windows.WmiBiosInfo
    WmiCliEventConsumers = windows.WmiCliEventConsumers
    WmiEventFilters = windows.WmiEventFilters
    WmiFilterConsumerBinding = windows.WmiFilterConsumerBinding
    WmiScriptEventConsumers = windows.WmiScriptEventConsumers
    # yara
    # yara_events


class Tables:
    _cross_platform: CrossPlatform
    freebsd: FreeBSD
    linux: Linux
    macos: MacOS
    windows: Windows

    def __init__(self, conn: Database):
        self._cross_platform = CrossPlatform(conn)
        self.freebsd = FreeBSD(conn)
        self.linux = Linux(conn)
        self.macos = MacOS(conn)
        self.windows = Windows(conn)
