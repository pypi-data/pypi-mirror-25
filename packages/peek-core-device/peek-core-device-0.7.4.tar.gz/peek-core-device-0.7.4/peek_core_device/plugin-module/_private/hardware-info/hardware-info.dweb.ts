import {DeviceTypeEnum, HardwareInfoI, webUuid} from "./hardware-info.abstract";
import {TupleOfflineStorageService} from "@synerty/vortexjs";

export class HardwareInfo implements HardwareInfoI {
    constructor( private tupleStorage: TupleOfflineStorageService) {

    }

    uuid(): Promise<string> {
        return webUuid(this.tupleStorage);
    }

    description(): string {
        return navigator.userAgent;
    }


    deviceType(): DeviceTypeEnum {
        return DeviceTypeEnum.DESKTOP_WEB;
    }
}