import {Component, OnInit} from "@angular/core";
import {
    ComponentLifecycleEventEmitter,
    TupleDataOfflineObserverService
} from "@synerty/vortexjs";
import {TitleService} from "@synerty/peek-util";
import {homeLinks} from "../../plugin-home-links";


@Component({
    selector: "peek-main-home",
    templateUrl: 'main-home.component.dweb.html',
    moduleId: module.id
})
export class MainHomeComponent extends ComponentLifecycleEventEmitter implements OnInit {

    appDetails = homeLinks;

    constructor(tupleDataObserver: TupleDataOfflineObserverService, titleService: TitleService) {
        super();
        titleService.setTitle("Peek Home");

    }

    ngOnInit() {
    }

    appButtonGridRows(): string {
        let val = "auto";
        for (let i = 0; i < this.appDetails.length / 2; i++) {
            val += ", auto";
        }
        return val;
    }

    appButtonGridRowIndex(index): number {
        return Math.floor(index / 2);
    }

}

