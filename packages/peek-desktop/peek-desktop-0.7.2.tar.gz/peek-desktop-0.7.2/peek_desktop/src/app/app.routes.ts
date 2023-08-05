import {MainHomeComponent} from "./main-home/main-home.component";
import {UnknownRouteComponent} from "./unknown-route/unknown-route.component";
import {pluginRoutes} from "../plugin-routes";
export const staticRoutes = [
    {
        path: "",
        component: MainHomeComponent,
        data: {title: "Home"}
    },
    ...pluginRoutes,
    {
        path: "**",
        component: UnknownRouteComponent,
        data: {title: "Route Error"}
    }
];