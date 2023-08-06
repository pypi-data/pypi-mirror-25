import {HardwareInfoI, DeviceTypeEnum} from "./hardware-info.abstract";
import {TupleOfflineStorageService} from "@synerty/vortexjs";

import * as app from "tns-core-modules/application";
import * as platform from "tns-core-modules/platform";

export class HardwareInfo implements HardwareInfoI {
    constructor( private tupleStorage: TupleOfflineStorageService) {

    }

    uuid(): Promise<string> {
        return Promise.resolve(platform.device.uuid);
    }

    description(): string {
        return `${platform.device.manufacturer}, ${platform.device.model}, ${platform.device.osVersion}`;
    }

    deviceType(): DeviceTypeEnum {
        if (app.android) {
            return DeviceTypeEnum.MOBILE_ANDROID;
        } else if (app.ios) {
            return DeviceTypeEnum.MOBILE_IOS;
        } else {
            throw new Error("Unknown native type");
        }
    }
}