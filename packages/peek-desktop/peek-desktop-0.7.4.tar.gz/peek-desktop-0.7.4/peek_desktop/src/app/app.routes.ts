import {MainHomeComponent} from "./main-home/main-home.component";
import {UnknownRouteComponent} from "./unknown-route/unknown-route.component";
import {pluginRoutes} from "../plugin-routes";

import {DeviceEnrolledGuard} from "@peek/peek_core_device";

export const staticRoutes = [
    {
        path: 'peek_core_device',
        loadChildren: "peek_core_device/device.module#DeviceModule"
    },
    // All routes require the device to be enrolled
    {
        path: '',
        canActivate: [DeviceEnrolledGuard],
        children: [
            {
                path: '',
                component: MainHomeComponent
            },
            ...pluginRoutes
        ]
    },
    {
        path: "**",
        component: UnknownRouteComponent
    }
];