import {Injectable} from "@angular/core";
import {CanActivate, ActivatedRouteSnapshot, RouterStateSnapshot} from "@angular/router";
import {TitleService} from "@synerty/peek-util";
import {DeviceEnrolmentService} from "./device-enrolment.service";
import {DeviceNavService} from "./_private/device-nav.service";
import {DeviceServerService} from "./_private/device-server.service";
import {Observable} from "rxjs";

@Injectable()
export class DeviceEnrolledGuard implements CanActivate {
    constructor(private enrolmentService: DeviceEnrolmentService,
                private nav: DeviceNavService,
                private titleService: TitleService,
                private serverService: DeviceServerService) {
    }

    canActivate(route: ActivatedRouteSnapshot,
                state: RouterStateSnapshot): Observable<boolean> | Promise<boolean> | boolean {

        console.log(route);

        if (!this.serverService.isSetup) {
            this.nav.toConnect();
            return false;
        }

        if (this.enrolmentService.isEnrolled()) {
            this.titleService.setEnabled(true);
            return true;
        }

        // This will take care of navigating to where to need to go to enroll
        this.enrolmentService.checkEnrolment();

        // Return true, otherwise the router just ends up in an infinite loop
        return false;
    }
}