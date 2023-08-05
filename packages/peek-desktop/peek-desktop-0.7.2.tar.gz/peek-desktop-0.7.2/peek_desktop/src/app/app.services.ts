import {Ng2BalloonMsgService} from "@synerty/ng2-balloon-msg";
import {VortexService, VortexStatusService} from "@synerty/vortexjs";
import {TitleService} from "@synerty/peek-util";
import {titleBarLinks} from "../plugin-title-bar-links";

export function titleServiceFactory() {
    return new TitleService(titleBarLinks);
}


export let peekRootServices = [
    {
        provide: TitleService,
        useFactory: titleServiceFactory
    },
    Ng2BalloonMsgService,

    // Vortex Services
    VortexStatusService,
    VortexService
];

