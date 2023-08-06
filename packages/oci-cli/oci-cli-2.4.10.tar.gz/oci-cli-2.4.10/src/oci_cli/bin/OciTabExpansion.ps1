$ociTopLevelCommands = @(
    'bv', 'compute', 'db', 'iam', 'network', 'os', 'setup'
)

$ociSubcommands = @{
    'bv' = 'volume backup'
    'bv backup' = 'create delete list update get'
    'bv volume' = 'create delete list update get'
    'compute' = 'instance instance-console-connection image console-history volume-attachment shape vnic-attachment'
    'compute console-history' = 'capture get list update get-content delete'
    'compute image' = 'get create list update export import delete'
    'compute image export' = 'to-object to-object-uri'
    'compute image import' = 'from-object-uri from-object'
    'compute instance' = 'get list attach-vnic terminate update launch get-windows-initial-creds action detach-vnic list-vnics'
    'compute instance-console-connection' = 'create delete list get'
    'compute shape' = 'list'
    'compute vnic-attachment' = 'list get'
    'compute volume-attachment' = 'attach detach list get'
    'db' = 'node database system system-shape version data-guard-association'
    'db data-guard-association' = 'switchover get create list reinstate failover'
    'db data-guard-association create' = 'from-existing-db-system'
    'db database' = 'create get list delete'
    'db node' = 'soft-reset reset get list stop start'
    'db system' = 'list get terminate update launch'
    'db system-shape' = 'list'
    'db version' = 'list'
    'iam' = 'customer-secret-key region-subscription region user availability-domain policy group compartment'
    'iam availability-domain' = 'list'
    'iam compartment' = 'create list update get'
    'iam customer-secret-key' = 'create list update delete'
    'iam group' = 'list-users add-user create get list update delete remove-user'
    'iam policy' = 'create delete list update get'
    'iam region' = 'list'
    'iam region-subscription' = 'create list'
    'iam user' = 'ui-password get create swift-password list update list-groups api-key update-user-state delete'
    'iam user api-key' = 'list upload delete'
    'iam user swift-password' = 'create list update delete'
    'iam user ui-password' = 'create-or-reset'
    'network' = 'vnic subnet security-list drg-attachment cpe vcn ip-sec-connection route-table internet-gateway private-ip dhcp-options drg'
    'network cpe' = 'create delete list update get'
    'network dhcp-options' = 'create delete list update get'
    'network drg' = 'create delete list update get'
    'network drg-attachment' = 'create delete list update get'
    'network internet-gateway' = 'create delete list update get'
    'network ip-sec-connection' = 'get-config get create list update get-status delete'
    'network private-ip' = 'delete list update get'
    'network route-table' = 'create delete list update get'
    'network security-list' = 'create delete list update get'
    'network subnet' = 'create delete list update get'
    'network vcn' = 'create delete list update get'
    'network vnic' = 'get assign-private-ip update unassign-private-ip'
    'os' = 'preauth-request ns bucket multipart object'
    'os bucket' = 'create get list update delete'
    'os multipart' = 'abort list'
    'os ns' = 'get'
    'os object' = 'bulk-download head get bulk-delete list resume-put put bulk-upload delete'
    'os preauth-request' = 'create delete list get'
    'setup' = 'keys autocomplete config'
}
$script:ociSubcommandKeys = $ociSubcommands.Keys -join '|'

$ociCommandsToLongParams = @{
    'bv backup create' = 'volume-id help generate-param-json-input display-name from-json generate-full-command-json-input'
    'bv backup delete' = 'volume-backup-id force help if-match generate-param-json-input from-json generate-full-command-json-input'
    'bv backup get' = 'volume-backup-id help from-json generate-param-json-input generate-full-command-json-input'
    'bv backup list' = 'volume-id help compartment-id limit generate-param-json-input page from-json generate-full-command-json-input'
    'bv backup update' = 'volume-backup-id help if-match generate-param-json-input display-name from-json generate-full-command-json-input'
    'bv volume create' = 'volume-backup-id size-in-mbs help size-in-gbs compartment-id generate-param-json-input availability-domain display-name from-json generate-full-command-json-input'
    'bv volume delete' = 'volume-id force help if-match generate-param-json-input from-json generate-full-command-json-input'
    'bv volume get' = 'volume-id help from-json generate-param-json-input generate-full-command-json-input'
    'bv volume list' = 'help compartment-id limit generate-param-json-input availability-domain page from-json generate-full-command-json-input'
    'bv volume update' = 'volume-id help if-match generate-param-json-input display-name from-json generate-full-command-json-input'
    'compute console-history capture' = 'help instance-id generate-param-json-input display-name from-json generate-full-command-json-input'
    'compute console-history delete' = 'instance-console-history-id force help if-match generate-param-json-input from-json generate-full-command-json-input'
    'compute console-history get' = 'instance-console-history-id help from-json generate-param-json-input generate-full-command-json-input'
    'compute console-history get-content' = 'instance-console-history-id file help length generate-param-json-input offset from-json generate-full-command-json-input'
    'compute console-history list' = 'help compartment-id limit from-json generate-param-json-input availability-domain page instance-id generate-full-command-json-input'
    'compute console-history update' = 'instance-console-history-id help if-match generate-param-json-input display-name from-json generate-full-command-json-input'
    'compute image create' = 'help compartment-id image-source-details generate-param-json-input display-name from-json instance-id generate-full-command-json-input'
    'compute image delete' = 'force help if-match generate-param-json-input image-id from-json generate-full-command-json-input'
    'compute image export to-object' = 'name help namespace bucket-name if-match generate-param-json-input image-id from-json generate-full-command-json-input'
    'compute image export to-object-uri' = 'help uri if-match generate-param-json-input image-id from-json generate-full-command-json-input'
    'compute image get' = 'generate-full-command-json-input help from-json generate-param-json-input image-id'
    'compute image import from-object' = 'name help namespace bucket-name compartment-id generate-param-json-input display-name from-json generate-full-command-json-input'
    'compute image import from-object-uri' = 'help uri compartment-id generate-param-json-input display-name from-json generate-full-command-json-input'
    'compute image list' = 'help operating-system-version compartment-id limit operating-system generate-param-json-input display-name page from-json generate-full-command-json-input'
    'compute image update' = 'help if-match generate-param-json-input image-id display-name from-json generate-full-command-json-input'
    'compute instance action' = 'help if-match generate-param-json-input action instance-id from-json generate-full-command-json-input'
    'compute instance attach-vnic' = 'assign-public-ip help vnic-display-name subnet-id hostname-label skip-source-dest-check from-json generate-param-json-input generate-full-command-json-input private-ip instance-id wait'
    'compute instance detach-vnic' = 'force help compartment-id generate-param-json-input vnic-id from-json generate-full-command-json-input'
    'compute instance get' = 'from-json help generate-param-json-input instance-id generate-full-command-json-input'
    'compute instance get-windows-initial-creds' = 'from-json help generate-param-json-input instance-id generate-full-command-json-input'
    'compute instance launch' = 'hostname-label assign-public-ip help private-ip extended-metadata ssh-authorized-keys-file subnet-id compartment-id ipxe-script-file shape skip-source-dest-check generate-param-json-input image-id user-data-file availability-domain display-name generate-full-command-json-input vnic-display-name from-json metadata'
    'compute instance list' = 'help compartment-id limit generate-param-json-input availability-domain display-name page from-json generate-full-command-json-input'
    'compute instance list-vnics' = 'help limit instance-id generate-param-json-input page from-json generate-full-command-json-input'
    'compute instance terminate' = 'force help if-match generate-param-json-input instance-id from-json generate-full-command-json-input'
    'compute instance update' = 'instance-id help if-match generate-param-json-input display-name from-json generate-full-command-json-input'
    'compute instance-console-connection create' = 'help ssh-public-key-file generate-param-json-input instance-id from-json generate-full-command-json-input'
    'compute instance-console-connection delete' = 'force help instance-console-connection-id if-match generate-param-json-input from-json generate-full-command-json-input'
    'compute instance-console-connection get' = 'instance-console-connection-id help from-json generate-param-json-input generate-full-command-json-input'
    'compute instance-console-connection list' = 'help compartment-id limit from-json generate-param-json-input page instance-id generate-full-command-json-input'
    'compute shape list' = 'help compartment-id limit generate-param-json-input image-id availability-domain page from-json generate-full-command-json-input'
    'compute vnic-attachment get' = 'from-json help generate-param-json-input vnic-attachment-id generate-full-command-json-input'
    'compute vnic-attachment list' = 'help vnic-id compartment-id limit from-json generate-param-json-input availability-domain page instance-id generate-full-command-json-input'
    'compute volume-attachment attach' = 'volume-id help from-json generate-param-json-input display-name type instance-id generate-full-command-json-input'
    'compute volume-attachment detach' = 'force help if-match generate-param-json-input volume-attachment-id from-json generate-full-command-json-input'
    'compute volume-attachment get' = 'volume-attachment-id help from-json generate-param-json-input generate-full-command-json-input'
    'compute volume-attachment list' = 'volume-id help compartment-id limit from-json generate-param-json-input availability-domain page instance-id generate-full-command-json-input'
    'db data-guard-association create from-existing-db-system' = 'creation-type help database-admin-password peer-db-system-id database-id from-json generate-param-json-input protection-mode transport-type generate-full-command-json-input'
    'db data-guard-association failover' = 'data-guard-association-id database-admin-password help database-id if-match generate-param-json-input from-json generate-full-command-json-input'
    'db data-guard-association get' = 'help database-id generate-param-json-input generate-full-command-json-input from-json data-guard-association-id'
    'db data-guard-association list' = 'help limit generate-param-json-input database-id page from-json generate-full-command-json-input'
    'db data-guard-association reinstate' = 'data-guard-association-id database-admin-password help database-id if-match generate-param-json-input from-json generate-full-command-json-input'
    'db data-guard-association switchover' = 'data-guard-association-id database-admin-password help database-id if-match generate-param-json-input from-json generate-full-command-json-input'
    'db database create' = 'db-system-id db-version pdb-name help ncharacter-set db-workload db-name generate-param-json-input character-set generate-full-command-json-input from-json admin-password'
    'db database delete' = 'force help database-id generate-param-json-input from-json generate-full-command-json-input'
    'db database get' = 'help database-id from-json generate-param-json-input generate-full-command-json-input'
    'db database list' = 'db-system-id help compartment-id limit generate-param-json-input from-json generate-full-command-json-input'
    'db node get' = 'from-json help db-node-id generate-param-json-input generate-full-command-json-input'
    'db node list' = 'db-system-id help compartment-id limit generate-param-json-input page from-json generate-full-command-json-input'
    'db node reset' = 'help db-node-id if-match generate-param-json-input from-json generate-full-command-json-input'
    'db node soft-reset' = 'help db-node-id if-match generate-param-json-input from-json generate-full-command-json-input'
    'db node start' = 'help db-node-id if-match generate-param-json-input from-json generate-full-command-json-input'
    'db node stop' = 'help db-node-id if-match generate-param-json-input from-json generate-full-command-json-input'
    'db system get' = 'from-json help generate-param-json-input db-system-id generate-full-command-json-input'
    'db system launch' = 'domain help pdb-name ncharacter-set license-model shape character-set display-name from-json admin-password database-edition db-version hostname compartment-id initial-data-storage-size-in-gb cluster-name generate-param-json-input db-workload disk-redundancy ssh-authorized-keys-file subnet-id backup-subnet-id cpu-core-count node-count db-name data-storage-percentage availability-domain generate-full-command-json-input'
    'db system list' = 'help compartment-id limit generate-param-json-input page from-json generate-full-command-json-input'
    'db system terminate' = 'force db-system-id help if-match generate-param-json-input from-json generate-full-command-json-input'
    'db system update' = 'force generate-param-json-input help ssh-authorized-keys-file if-match db-system-id from-json data-storage-size-in-gb cpu-core-count generate-full-command-json-input'
    'db system-shape list' = 'help compartment-id limit generate-param-json-input availability-domain page from-json generate-full-command-json-input'
    'db version list' = 'help db-system-shape compartment-id limit generate-param-json-input page from-json generate-full-command-json-input'
    'iam availability-domain list' = 'compartment-id help from-json generate-param-json-input generate-full-command-json-input'
    'iam compartment create' = 'name description help compartment-id generate-param-json-input from-json generate-full-command-json-input'
    'iam compartment get' = 'compartment-id help from-json generate-param-json-input generate-full-command-json-input'
    'iam compartment list' = 'help compartment-id limit generate-param-json-input page from-json generate-full-command-json-input'
    'iam compartment update' = 'description help name compartment-id if-match generate-param-json-input from-json generate-full-command-json-input'
    'iam customer-secret-key create' = 'help generate-param-json-input display-name user-id from-json generate-full-command-json-input'
    'iam customer-secret-key delete' = 'customer-secret-key-id force help if-match generate-param-json-input user-id from-json generate-full-command-json-input'
    'iam customer-secret-key list' = 'user-id help from-json generate-param-json-input generate-full-command-json-input'
    'iam customer-secret-key update' = 'customer-secret-key-id help if-match generate-param-json-input user-id display-name from-json generate-full-command-json-input'
    'iam group add-user' = 'help generate-param-json-input user-id generate-full-command-json-input from-json group-id'
    'iam group create' = 'name description help compartment-id generate-param-json-input from-json generate-full-command-json-input'
    'iam group delete' = 'force group-id help if-match generate-param-json-input from-json generate-full-command-json-input'
    'iam group get' = 'from-json help group-id generate-param-json-input generate-full-command-json-input'
    'iam group list' = 'help compartment-id limit generate-param-json-input page from-json generate-full-command-json-input'
    'iam group list-users' = 'group-id help compartment-id limit generate-param-json-input page from-json generate-full-command-json-input'
    'iam group remove-user' = 'force group-id help compartment-id generate-param-json-input user-id from-json generate-full-command-json-input'
    'iam group update' = 'group-id description help if-match generate-param-json-input from-json generate-full-command-json-input'
    'iam policy create' = 'version-date statements name description help compartment-id generate-param-json-input from-json generate-full-command-json-input'
    'iam policy delete' = 'force help policy-id if-match generate-param-json-input from-json generate-full-command-json-input'
    'iam policy get' = 'policy-id help from-json generate-param-json-input generate-full-command-json-input'
    'iam policy list' = 'help compartment-id limit generate-param-json-input page from-json generate-full-command-json-input'
    'iam policy update' = 'version-date force description policy-id help if-match generate-param-json-input statements from-json generate-full-command-json-input'
    'iam region list' = 'help from-json generate-param-json-input generate-full-command-json-input'
    'iam region-subscription create' = 'tenancy-id help region-key generate-param-json-input from-json generate-full-command-json-input'
    'iam region-subscription list' = 'tenancy-id help from-json generate-param-json-input generate-full-command-json-input'
    'iam user api-key delete' = 'force help if-match generate-param-json-input fingerprint user-id from-json generate-full-command-json-input'
    'iam user api-key list' = 'user-id help from-json generate-param-json-input generate-full-command-json-input'
    'iam user api-key upload' = 'key help generate-param-json-input user-id from-json generate-full-command-json-input'
    'iam user create' = 'name description help compartment-id generate-param-json-input from-json generate-full-command-json-input'
    'iam user delete' = 'force help if-match generate-param-json-input user-id from-json generate-full-command-json-input'
    'iam user get' = 'user-id help from-json generate-param-json-input generate-full-command-json-input'
    'iam user list' = 'help compartment-id limit generate-param-json-input page from-json generate-full-command-json-input'
    'iam user list-groups' = 'help compartment-id limit generate-param-json-input user-id page from-json generate-full-command-json-input'
    'iam user swift-password create' = 'help generate-param-json-input user-id generate-full-command-json-input from-json description'
    'iam user swift-password delete' = 'force help if-match generate-param-json-input swift-password-id user-id from-json generate-full-command-json-input'
    'iam user swift-password list' = 'user-id help from-json generate-param-json-input generate-full-command-json-input'
    'iam user swift-password update' = 'description help if-match generate-param-json-input swift-password-id user-id from-json generate-full-command-json-input'
    'iam user ui-password create-or-reset' = 'user-id help from-json generate-param-json-input generate-full-command-json-input'
    'iam user update' = 'description help if-match generate-param-json-input user-id from-json generate-full-command-json-input'
    'iam user update-user-state' = 'help if-match generate-param-json-input user-id blocked from-json generate-full-command-json-input'
    'network cpe create' = 'ip-address help compartment-id generate-param-json-input display-name from-json generate-full-command-json-input'
    'network cpe delete' = 'force cpe-id help if-match generate-param-json-input from-json generate-full-command-json-input'
    'network cpe get' = 'from-json help generate-param-json-input cpe-id generate-full-command-json-input'
    'network cpe list' = 'help compartment-id limit generate-param-json-input page from-json generate-full-command-json-input'
    'network cpe update' = 'cpe-id help if-match generate-param-json-input display-name from-json generate-full-command-json-input'
    'network dhcp-options create' = 'help vcn-id compartment-id generate-param-json-input display-name options from-json generate-full-command-json-input'
    'network dhcp-options delete' = 'force dhcp-id help if-match generate-param-json-input from-json generate-full-command-json-input'
    'network dhcp-options get' = 'from-json help generate-param-json-input dhcp-id generate-full-command-json-input'
    'network dhcp-options list' = 'help vcn-id compartment-id limit generate-param-json-input page from-json generate-full-command-json-input'
    'network dhcp-options update' = 'force generate-param-json-input help if-match dhcp-id display-name options from-json generate-full-command-json-input'
    'network drg create' = 'help compartment-id generate-param-json-input display-name from-json generate-full-command-json-input'
    'network drg delete' = 'force help if-match generate-param-json-input drg-id from-json generate-full-command-json-input'
    'network drg get' = 'generate-full-command-json-input help from-json generate-param-json-input drg-id'
    'network drg list' = 'help compartment-id limit generate-param-json-input page from-json generate-full-command-json-input'
    'network drg update' = 'help if-match generate-param-json-input drg-id display-name from-json generate-full-command-json-input'
    'network drg-attachment create' = 'help vcn-id generate-param-json-input drg-id display-name from-json generate-full-command-json-input'
    'network drg-attachment delete' = 'force help drg-attachment-id if-match generate-param-json-input from-json generate-full-command-json-input'
    'network drg-attachment get' = 'help drg-attachment-id from-json generate-param-json-input generate-full-command-json-input'
    'network drg-attachment list' = 'help vcn-id compartment-id limit generate-param-json-input drg-id page from-json generate-full-command-json-input'
    'network drg-attachment update' = 'help drg-attachment-id if-match generate-param-json-input display-name from-json generate-full-command-json-input'
    'network internet-gateway create' = 'is-enabled vcn-id help compartment-id generate-param-json-input display-name from-json generate-full-command-json-input'
    'network internet-gateway delete' = 'force help ig-id if-match generate-param-json-input from-json generate-full-command-json-input'
    'network internet-gateway get' = 'generate-full-command-json-input help from-json generate-param-json-input ig-id'
    'network internet-gateway list' = 'help vcn-id compartment-id limit generate-param-json-input page from-json generate-full-command-json-input'
    'network internet-gateway update' = 'is-enabled ig-id help if-match generate-param-json-input display-name from-json generate-full-command-json-input'
    'network ip-sec-connection create' = 'generate-param-json-input help static-routes compartment-id cpe-id drg-id display-name from-json generate-full-command-json-input'
    'network ip-sec-connection delete' = 'force help if-match generate-param-json-input generate-full-command-json-input from-json ipsc-id'
    'network ip-sec-connection get' = 'from-json help generate-param-json-input ipsc-id generate-full-command-json-input'
    'network ip-sec-connection get-config' = 'from-json help generate-param-json-input ipsc-id generate-full-command-json-input'
    'network ip-sec-connection get-status' = 'from-json help generate-param-json-input ipsc-id generate-full-command-json-input'
    'network ip-sec-connection list' = 'generate-param-json-input help compartment-id limit cpe-id drg-id page from-json generate-full-command-json-input'
    'network ip-sec-connection update' = 'help if-match generate-param-json-input display-name generate-full-command-json-input from-json ipsc-id'
    'network private-ip delete' = 'force help private-ip-id if-match generate-param-json-input from-json generate-full-command-json-input'
    'network private-ip get' = 'private-ip-id help from-json generate-param-json-input generate-full-command-json-input'
    'network private-ip list' = 'generate-param-json-input help subnet-id vnic-id limit ip-address page from-json generate-full-command-json-input'
    'network private-ip update' = 'hostname-label help private-ip-id if-match generate-param-json-input display-name from-json generate-full-command-json-input'
    'network route-table create' = 'help route-rules vcn-id compartment-id generate-param-json-input display-name from-json generate-full-command-json-input'
    'network route-table delete' = 'force help if-match generate-param-json-input rt-id from-json generate-full-command-json-input'
    'network route-table get' = 'rt-id help from-json generate-param-json-input generate-full-command-json-input'
    'network route-table list' = 'help vcn-id compartment-id limit generate-param-json-input page from-json generate-full-command-json-input'
    'network route-table update' = 'force help route-rules if-match generate-param-json-input rt-id display-name from-json generate-full-command-json-input'
    'network security-list create' = 'ingress-security-rules help vcn-id compartment-id generate-param-json-input egress-security-rules display-name from-json generate-full-command-json-input'
    'network security-list delete' = 'force help security-list-id if-match generate-param-json-input from-json generate-full-command-json-input'
    'network security-list get' = 'generate-full-command-json-input help from-json generate-param-json-input security-list-id'
    'network security-list list' = 'help vcn-id compartment-id limit generate-param-json-input page from-json generate-full-command-json-input'
    'network security-list update' = 'force help security-list-id if-match generate-param-json-input egress-security-rules ingress-security-rules display-name from-json generate-full-command-json-input'
    'network subnet create' = 'help vcn-id route-table-id cidr-block compartment-id dhcp-options-id generate-param-json-input availability-domain display-name generate-full-command-json-input prohibit-public-ip-on-vnic dns-label from-json security-list-ids'
    'network subnet delete' = 'force help subnet-id if-match generate-param-json-input from-json generate-full-command-json-input'
    'network subnet get' = 'from-json help generate-param-json-input subnet-id generate-full-command-json-input'
    'network subnet list' = 'help vcn-id compartment-id limit generate-param-json-input page from-json generate-full-command-json-input'
    'network subnet update' = 'help subnet-id if-match generate-param-json-input display-name from-json generate-full-command-json-input'
    'network vcn create' = 'help cidr-block compartment-id generate-param-json-input display-name dns-label from-json generate-full-command-json-input'
    'network vcn delete' = 'force help vcn-id if-match generate-param-json-input from-json generate-full-command-json-input'
    'network vcn get' = 'generate-full-command-json-input help from-json generate-param-json-input vcn-id'
    'network vcn list' = 'help compartment-id limit generate-param-json-input page from-json generate-full-command-json-input'
    'network vcn update' = 'help vcn-id if-match generate-param-json-input display-name from-json generate-full-command-json-input'
    'network vnic assign-private-ip' = 'ip-address unassign-if-already-assigned help hostname-label generate-param-json-input display-name vnic-id from-json generate-full-command-json-input'
    'network vnic get' = 'from-json help vnic-id generate-param-json-input generate-full-command-json-input'
    'network vnic unassign-private-ip' = 'help generate-param-json-input ip-address vnic-id from-json generate-full-command-json-input'
    'network vnic update' = 'help hostname-label if-match generate-param-json-input display-name skip-source-dest-check vnic-id from-json generate-full-command-json-input'
    'os bucket create' = 'help name public-access-type namespace compartment-id generate-param-json-input metadata from-json generate-full-command-json-input'
    'os bucket delete' = 'force name help namespace if-match generate-param-json-input from-json generate-full-command-json-input'
    'os bucket get' = 'name help namespace if-match generate-param-json-input if-none-match from-json generate-full-command-json-input'
    'os bucket list' = 'help namespace compartment-id limit generate-param-json-input page from-json generate-full-command-json-input'
    'os bucket update' = 'help name public-access-type namespace if-match generate-param-json-input metadata from-json generate-full-command-json-input'
    'os multipart abort' = 'force help upload-id namespace bucket-name object-name generate-param-json-input from-json generate-full-command-json-input'
    'os multipart list' = 'help namespace bucket-name limit generate-param-json-input page from-json generate-full-command-json-input'
    'os ns get' = 'help from-json generate-param-json-input generate-full-command-json-input'
    'os object bulk-delete' = 'dry-run help parallel-operations-count namespace prefix bucket-name delimiter generate-param-json-input exclude force include from-json generate-full-command-json-input'
    'os object bulk-download' = 'no-overwrite help parallel-operations-count namespace prefix download-dir bucket-name delimiter from-json generate-param-json-input exclude include overwrite generate-full-command-json-input'
    'os object bulk-upload' = 'help no-overwrite content-language src-dir disable-parallel-uploads no-multipart object-prefix namespace bucket-name generate-param-json-input content-encoding from-json parallel-upload-count generate-full-command-json-input exclude include content-type part-size overwrite metadata'
    'os object delete' = 'force name help namespace bucket-name if-match generate-param-json-input from-json generate-full-command-json-input'
    'os object get' = 'name help generate-param-json-input namespace bucket-name range if-match file if-none-match from-json generate-full-command-json-input'
    'os object head' = 'name help namespace bucket-name if-match generate-param-json-input if-none-match from-json generate-full-command-json-input'
    'os object list' = 'end help delimiter namespace bucket-name start prefix limit generate-param-json-input fields from-json generate-full-command-json-input'
    'os object put' = 'help force name content-language content-encoding disable-parallel-uploads no-multipart generate-param-json-input namespace bucket-name content-md5 if-match file parallel-upload-count generate-full-command-json-input content-type part-size from-json metadata'
    'os object resume-put' = 'name help part-size generate-param-json-input namespace bucket-name disable-parallel-uploads file parallel-upload-count upload-id from-json generate-full-command-json-input'
    'os preauth-request create' = 'time-expires name opc-client-request-id help namespace bucket-name object-name generate-param-json-input access-type from-json generate-full-command-json-input'
    'os preauth-request delete' = 'force help opc-client-request-id par-id namespace bucket-name generate-param-json-input from-json generate-full-command-json-input'
    'os preauth-request get' = 'help opc-client-request-id par-id namespace bucket-name generate-param-json-input from-json generate-full-command-json-input'
    'os preauth-request list' = 'generate-param-json-input opc-client-request-id help namespace bucket-name limit object-name-prefix page from-json generate-full-command-json-input'
    'setup autocomplete' = 'help'
    'setup config' = 'help'
    'setup keys' = 'help output-dir key-name passphrase passphrase-file overwrite'
}
$script:ociCommandsWithLongParams = $ociCommandsToLongParams.Keys -join '|'

$ociCommandsToShortParams = @{
    'bv backup create' = 'h ?'
    'bv backup delete' = 'h ?'
    'bv backup get' = 'h ?'
    'bv backup list' = 'h c ?'
    'bv backup update' = 'h ?'
    'bv volume create' = 'h c ?'
    'bv volume delete' = 'h ?'
    'bv volume get' = 'h ?'
    'bv volume list' = 'h c ?'
    'bv volume update' = 'h ?'
    'compute console-history capture' = 'h ?'
    'compute console-history delete' = 'h ?'
    'compute console-history get' = 'h ?'
    'compute console-history get-content' = 'h ?'
    'compute console-history list' = 'h c ?'
    'compute console-history update' = 'h ?'
    'compute image create' = 'h c ?'
    'compute image delete' = 'h ?'
    'compute image export to-object' = 'h bn ns ?'
    'compute image export to-object-uri' = 'h ?'
    'compute image get' = 'h ?'
    'compute image import from-object' = 'h c ns bn ?'
    'compute image import from-object-uri' = 'h c ?'
    'compute image list' = 'h c ?'
    'compute image update' = 'h ?'
    'compute instance action' = 'h ?'
    'compute instance attach-vnic' = 'h ?'
    'compute instance detach-vnic' = 'h c ?'
    'compute instance get' = 'h ?'
    'compute instance get-windows-initial-creds' = 'h ?'
    'compute instance launch' = 'h c ?'
    'compute instance list' = 'h c ?'
    'compute instance list-vnics' = 'h ?'
    'compute instance terminate' = 'h ?'
    'compute instance update' = 'h ?'
    'compute instance-console-connection create' = 'h ?'
    'compute instance-console-connection delete' = 'h ?'
    'compute instance-console-connection get' = 'h ?'
    'compute instance-console-connection list' = 'h c ?'
    'compute shape list' = 'h c ?'
    'compute vnic-attachment get' = 'h ?'
    'compute vnic-attachment list' = 'h c ?'
    'compute volume-attachment attach' = 'h ?'
    'compute volume-attachment detach' = 'h ?'
    'compute volume-attachment get' = 'h ?'
    'compute volume-attachment list' = 'h c ?'
    'db data-guard-association create from-existing-db-system' = 'h ?'
    'db data-guard-association failover' = 'h ?'
    'db data-guard-association get' = 'h ?'
    'db data-guard-association list' = 'h ?'
    'db data-guard-association reinstate' = 'h ?'
    'db data-guard-association switchover' = 'h ?'
    'db database create' = 'h ?'
    'db database delete' = 'h ?'
    'db database get' = 'h ?'
    'db database list' = 'h c ?'
    'db node get' = 'h ?'
    'db node list' = 'h c ?'
    'db node reset' = 'h ?'
    'db node soft-reset' = 'h ?'
    'db node start' = 'h ?'
    'db node stop' = 'h ?'
    'db system get' = 'h ?'
    'db system launch' = 'h c ?'
    'db system list' = 'h c ?'
    'db system terminate' = 'h ?'
    'db system update' = 'h ?'
    'db system-shape list' = 'h c ?'
    'db version list' = 'h c ?'
    'iam availability-domain list' = 'h c ?'
    'iam compartment create' = 'h c ?'
    'iam compartment get' = 'h c ?'
    'iam compartment list' = 'h c ?'
    'iam compartment update' = 'h c ?'
    'iam customer-secret-key create' = 'h ?'
    'iam customer-secret-key delete' = 'h ?'
    'iam customer-secret-key list' = 'h ?'
    'iam customer-secret-key update' = 'h ?'
    'iam group add-user' = 'h ?'
    'iam group create' = 'h c ?'
    'iam group delete' = 'h ?'
    'iam group get' = 'h ?'
    'iam group list' = 'h c ?'
    'iam group list-users' = 'h c ?'
    'iam group remove-user' = 'h c ?'
    'iam group update' = 'h ?'
    'iam policy create' = 'h c ?'
    'iam policy delete' = 'h ?'
    'iam policy get' = 'h ?'
    'iam policy list' = 'h c ?'
    'iam policy update' = 'h ?'
    'iam region list' = 'h ?'
    'iam region-subscription create' = 'h ?'
    'iam region-subscription list' = 'h ?'
    'iam user api-key delete' = 'h ?'
    'iam user api-key list' = 'h ?'
    'iam user api-key upload' = 'h ?'
    'iam user create' = 'h c ?'
    'iam user delete' = 'h ?'
    'iam user get' = 'h ?'
    'iam user list' = 'h c ?'
    'iam user list-groups' = 'h c ?'
    'iam user swift-password create' = 'h ?'
    'iam user swift-password delete' = 'h ?'
    'iam user swift-password list' = 'h ?'
    'iam user swift-password update' = 'h ?'
    'iam user ui-password create-or-reset' = 'h ?'
    'iam user update' = 'h ?'
    'iam user update-user-state' = 'h ?'
    'network cpe create' = 'h c ?'
    'network cpe delete' = 'h ?'
    'network cpe get' = 'h ?'
    'network cpe list' = 'h c ?'
    'network cpe update' = 'h ?'
    'network dhcp-options create' = 'h c ?'
    'network dhcp-options delete' = 'h ?'
    'network dhcp-options get' = 'h ?'
    'network dhcp-options list' = 'h c ?'
    'network dhcp-options update' = 'h ?'
    'network drg create' = 'h c ?'
    'network drg delete' = 'h ?'
    'network drg get' = 'h ?'
    'network drg list' = 'h c ?'
    'network drg update' = 'h ?'
    'network drg-attachment create' = 'h ?'
    'network drg-attachment delete' = 'h ?'
    'network drg-attachment get' = 'h ?'
    'network drg-attachment list' = 'h c ?'
    'network drg-attachment update' = 'h ?'
    'network internet-gateway create' = 'h c ?'
    'network internet-gateway delete' = 'h ?'
    'network internet-gateway get' = 'h ?'
    'network internet-gateway list' = 'h c ?'
    'network internet-gateway update' = 'h ?'
    'network ip-sec-connection create' = 'h c ?'
    'network ip-sec-connection delete' = 'h ?'
    'network ip-sec-connection get' = 'h ?'
    'network ip-sec-connection get-config' = 'h ?'
    'network ip-sec-connection get-status' = 'h ?'
    'network ip-sec-connection list' = 'h c ?'
    'network ip-sec-connection update' = 'h ?'
    'network private-ip delete' = 'h ?'
    'network private-ip get' = 'h ?'
    'network private-ip list' = 'h ?'
    'network private-ip update' = 'h ?'
    'network route-table create' = 'h c ?'
    'network route-table delete' = 'h ?'
    'network route-table get' = 'h ?'
    'network route-table list' = 'h c ?'
    'network route-table update' = 'h ?'
    'network security-list create' = 'h c ?'
    'network security-list delete' = 'h ?'
    'network security-list get' = 'h ?'
    'network security-list list' = 'h c ?'
    'network security-list update' = 'h ?'
    'network subnet create' = 'h c ?'
    'network subnet delete' = 'h ?'
    'network subnet get' = 'h ?'
    'network subnet list' = 'h c ?'
    'network subnet update' = 'h ?'
    'network vcn create' = 'h c ?'
    'network vcn delete' = 'h ?'
    'network vcn get' = 'h ?'
    'network vcn list' = 'h c ?'
    'network vcn update' = 'h ?'
    'network vnic assign-private-ip' = 'h ?'
    'network vnic get' = 'h ?'
    'network vnic unassign-private-ip' = 'h ?'
    'network vnic update' = 'h ?'
    'os bucket create' = 'h c ns ?'
    'os bucket delete' = 'h ns ?'
    'os bucket get' = 'h ns ?'
    'os bucket list' = 'h c ns ?'
    'os bucket update' = 'h ns ?'
    'os multipart abort' = 'on bn ns ? h'
    'os multipart list' = 'h bn ns ?'
    'os ns get' = 'h ?'
    'os object bulk-delete' = 'h bn ns ?'
    'os object bulk-download' = 'h bn ns ?'
    'os object bulk-upload' = 'h bn ns ?'
    'os object delete' = 'h bn ns ?'
    'os object get' = 'h bn ns ?'
    'os object head' = 'h bn ns ?'
    'os object list' = 'h bn ns ?'
    'os object put' = 'h bn ns ?'
    'os object resume-put' = 'h bn ns ?'
    'os preauth-request create' = 'on bn ns ? h'
    'os preauth-request delete' = 'h bn ns ?'
    'os preauth-request get' = 'h bn ns ?'
    'os preauth-request list' = 'h bn ns ?'
    'setup autocomplete' = 'h ?'
    'setup config' = 'h ?'
    'setup keys' = 'h ?'
}
$script:ociCommandsWithShortParams = $ociCommandsToShortParams.Keys -join '|'

function OciTabExpansion($lastBlock) {
    $res = Oci-Invoke-Utf8ConsoleCommand { OciTabExpansionInternal $lastBlock }
	$res
}

function OciTabExpansionInternal($lastBlock) {
	$ociAliasPattern = GetOciAliasPattern 
	
	switch -regex ($lastBlock -replace "^$($ociAliasPattern) ","") {
		# Handles [oci|bmcs] <top-level command>
		"^(?<cmd>\w+?)$" {
            $com = $matches['cmd']
			$ociTopLevelCommands | Where-Object { $_ -like "$com*" }
		}
	
		# Handles [oci|bmcs] <top-level command> <sub-command> <sub-command> ...
        "^(?<cmd>$ociSubcommandKeys)\s+(?<op>\S*)$" {
            ociCmdOperations $ociSubcommands $matches['cmd'] $matches['op']
        }
		
		# Handles [oci|bmcs] <some level of commands> --<param>
        "^(?<cmd>$ociCommandsWithLongParams).* --(?<param>\S*)$" {
            expandOciLongParams $matches['cmd'] $matches['param']
        }

        # Handles [oci|bmcs] <some level of commands> -<shortparam>
        "^(?<cmd>$ociCommandsWithShortParams).* -(?<shortparam>\S*)$" {
            expandOciShortParams $matches['cmd'] $matches['shortparam']
        }
	}
}

function script:ociCmdOperations($commands, $command, $filter) {
    $commands.$command -split ' ' | Where-Object { $_ -like "$filter*" }
}

function script:expandOciLongParams($cmd, $filter) {
    $ociCommandsToLongParams[$cmd] -split ' ' |
        Where-Object { $_ -like "$filter*" } |
        Sort-Object |
        ForEach-Object { -join ("--", $_) }
}

function script:expandOciShortParams($cmd, $filter) {
    $ociCommandsToShortParams[$cmd] -split ' ' |
        Where-Object { $_ -like "$filter*" } |
        Sort-Object |
        ForEach-Object { -join ("-", $_) }
}

function GetOciAliasPattern() {
	$ociAliases = @("oci", "bmcs") + @(Get-Alias | where { $_.Definition -eq "oci" } | select -Exp Name) + @(Get-Alias | where { $_.Definition -eq "bmcs" } | select -Exp Name)
	$ociAliasPattern = "($($ociAliases -join '|'))"
	
	return $ociAliasPattern
}

function Oci-Invoke-Utf8ConsoleCommand([ScriptBlock]$cmd) {
    $currentEncoding = [Console]::OutputEncoding
    $errorCount = $global:Error.Count
    try {
        # A native executable that writes to stderr AND has its stderr redirected will generate non-terminating
        # error records if the user has set $ErrorActionPreference to Stop. Override that value in this scope.
        $ErrorActionPreference = 'Continue'
        if ($currentEncoding.IsSingleByte) {
            [Console]::OutputEncoding = [Text.Encoding]::UTF8
        }
        & $cmd
    }
    finally {
        if ($currentEncoding.IsSingleByte) {
            [Console]::OutputEncoding = $currentEncoding
        }

        # Clear out stderr output that was added to the $Error collection, putting those errors in a module variable
        if ($global:Error.Count -gt $errorCount) {
            $numNewErrors = $global:Error.Count - $errorCount
            $invokeErrors.InsertRange(0, $global:Error.GetRange(0, $numNewErrors))
            if ($invokeErrors.Count -gt 256) {
                $invokeErrors.RemoveRange(256, ($invokeErrors.Count - 256))
            }
            $global:Error.RemoveRange(0, $numNewErrors)
        }
    }
}

if (Test-Path Function:\TabExpansion) {
    Rename-Item Function:\TabExpansion TabExpansionBackupFromOciAutocomplete
}

function TabExpansion($line, $lastWord) {
    $lastBlock = [regex]::Split($line, '[|;]')[-1].TrimStart()

	$ociAliasPattern = GetOciAliasPattern
	
	switch -regex ($lastBlock) {
        # Execute OCI/BMCS tab completion
        "^$($ociAliasPattern) (.*)" { OciTabExpansion $lastBlock }

        # Fall back on existing tab expansion
        default {
            if (Test-Path Function:\TabExpansionBackupFromOciAutocomplete) {
                TabExpansionBackupFromOciAutocomplete $line $lastWord
            }
        }
    }
}