import {Injectable, NgZone} from "@angular/core";
import {
    TupleActionPushOfflineSingletonService,
    TupleDataObservableNameService,
    TupleDataObserverService,
    TupleDataOfflineObserverService,
    TupleOfflineStorageNameService,
    TupleOfflineStorageService,
    VortexService,
    VortexStatusService,
    TupleActionPushNameService,
    TupleActionPushOfflineService,
    TupleStorageFactoryService
} from "@synerty/vortexjs";

import {
    deviceActionProcessorName,
    deviceFilt,
    deviceObservableName,
    deviceTupleOfflineServiceName
} from "./PluginNames";
import {HardwareInfo} from "./hardware-info/hardware-info.mweb";


/** Device Tuple Service
 *
 * This service provides the tuple action, observable and storage classes for the
 * other services in this plugin.
 *
 * Since there are sevaral services setting up their own instances of these, it made
 * sense to combine them all.
 *
 */
@Injectable()
export class DeviceTupleService {
    offlineStorage: TupleOfflineStorageService;
    offlineObserver: TupleDataObserverService;
    observer: TupleDataObserverService;
    tupleOfflineAction: TupleActionPushOfflineService;

    hardwareInfo: HardwareInfo;

    constructor(storageFactory: TupleStorageFactoryService,
                actionSingletonService: TupleActionPushOfflineSingletonService,
                vortexService: VortexService,
                vortexStatusService: VortexStatusService,
                zone: NgZone) {

        // Create the offline storage
        this.offlineStorage = new TupleOfflineStorageService(
            storageFactory,
            new TupleOfflineStorageNameService(deviceTupleOfflineServiceName)
        );

        // Create the offline observer
        this.offlineObserver = new TupleDataOfflineObserverService(
            vortexService,
            vortexStatusService,
            zone,
            new TupleDataObservableNameService(
                deviceObservableName,
                deviceFilt),
            this.offlineStorage
        );

        // Create the observer
        this.observer = new TupleDataObserverService(
            vortexService,
            vortexStatusService,
            zone,
            new TupleDataObservableNameService(
                deviceObservableName,
                deviceFilt)
        );

        // Create the observer
        this.tupleOfflineAction = new TupleActionPushOfflineService(
            new TupleActionPushNameService(deviceActionProcessorName, deviceFilt),
            vortexService,
            vortexStatusService,
            actionSingletonService
        );

        this.hardwareInfo = new HardwareInfo(this.offlineStorage);

    }


}