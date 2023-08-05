import {MainHomeComponent} from "./main-home/main-home.component";
import {UnknownRouteComponent} from "./unknown-route/unknown-route.component";

import {DeviceEnrolledGuard} from "@peek/peek_core_device";

import {pluginRoutes} from "../plugin-routes";

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