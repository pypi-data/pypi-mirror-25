// This file is auto generated, the git version is blank and .gitignored
export const pluginRoutes = [
    {
        path: 'peek_core_device',
        loadChildren: "peek_core_device/device.module#DeviceModule"
    },
    {
        path: 'peek_plugin_chat',
        loadChildren: "peek_plugin_chat/chat.module#ChatModule"
    },
    {
        path: 'peek_plugin_diagram',
        loadChildren: "peek_plugin_diagram/diagram.module.web#PeekPluginDiagramModule"
    },
    {
        path: 'peek_plugin_gis_diagram',
        loadChildren: "peek_plugin_gis_diagram/gisDiagram.module#GisDiagramModule"
    },
    {
        path: 'peek_plugin_gis_diagram_loader',
        loadChildren: "peek_plugin_gis_diagram_loader/gisDiagramLoader.module#GisDiagramLoaderModule"
    },
    {
        path: 'peek_plugin_inbox',
        loadChildren: "peek_plugin_inbox/plugin-inbox.module#PluginInboxAdminModule"
    },
    {
        path: 'peek_plugin_livedb',
        loadChildren: "peek_plugin_livedb/livedb.module#LiveDBModule"
    },
    {
        path: 'peek_plugin_pof_diagram',
        loadChildren: "peek_plugin_pof_diagram/pofDiagram.module#PofDiagramModule"
    },
    {
        path: 'peek_plugin_pof_diagram_loader',
        loadChildren: "peek_plugin_pof_diagram_loader/pofDiagramLoader.module#PofDiagramLoaderModule"
    },
    {
        path: 'peek_plugin_pof_field_incidents',
        loadChildren: "peek_plugin_pof_field_incidents/field-incidents-admin.module#PofFieldIncidentsAdminModule"
    },
    {
        path: 'peek_plugin_pof_field_switching',
        loadChildren: "peek_plugin_pof_field_switching/plugin-pof-field-switching.module#PluginPofFieldSwitchingAdminModule"
    },
    {
        path: 'peek_plugin_pof_livedb_loader',
        loadChildren: "peek_plugin_pof_livedb_loader/pofLivedbLoader.module#PofLivedbLoaderModule"
    },
    {
        path: 'peek_plugin_pof_soap',
        loadChildren: "peek_plugin_pof_soap/plugin-pof-soap.module"
    },
    {
        path: 'peek_plugin_pof_sql',
        loadChildren: "peek_plugin_pof_sql/plugin-pof-sql.module"
    },
    {
        path: 'peek_plugin_user',
        loadChildren: "peek_plugin_user/plugin-user.module#PluginUserDbAdminModule"
    }
];
