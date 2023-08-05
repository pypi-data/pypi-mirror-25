import {Injectable} from "@angular/core";
import {Ng2BalloonMsgService} from "@synerty/ng2-balloon-msg";
import {
    addTupleType,
    extend,
    Tuple,
    TupleSelector,
    VortexService,
    VortexStatusService
} from "@synerty/vortexjs";

import {deviceFilt, deviceTuplePrefix} from "./PluginNames";
import {DeviceTypeEnum} from "./hardware-info/hardware-info.abstract";
import {DeviceTupleService} from "./device-tuple.service";
import {DeviceNavService} from "./device-nav.service";
import {Observable, Subject} from "rxjs";

@addTupleType
export class ServerInfoTuple extends Tuple {
    public static readonly tupleName = deviceTuplePrefix + "ServerInfoTuple";

    host: string;
    useSsl: boolean = false;
    httpPort: number = 8000;
    websocketPort: number = 8001;
    hasConnected: boolean = false;

    constructor() {
        super(ServerInfoTuple.tupleName);
    }
}


@Injectable()
export class DeviceServerService {

    private tupleSelector: TupleSelector = new TupleSelector(
        ServerInfoTuple.tupleName, {}
    );

    private serverInfo: ServerInfoTuple = new ServerInfoTuple();
    private serverInfoSubject = new Subject<ServerInfoTuple>();

    private readonly deviceOnlineFilt = extend({key: "device.online"}, deviceFilt);

    private lastOnlineSub: any | null = null;

    constructor(private nav: DeviceNavService,
                private balloonMsg: Ng2BalloonMsgService,
                private vortexService: VortexService,
                private vortexStatusService: VortexStatusService,
                private tupleService: DeviceTupleService) {

        let type: DeviceTypeEnum = this.tupleService.hardwareInfo.deviceType();

        this.loadConnInfo()
            .then(() => {

                // If there is a host set, set the vortex
                if (this.isSetup) {
                    this.updateVortex();
                } else {
                    this.nav.toConnect();
                }
            });

    }

    get connInfoObserver(): Observable<ServerInfoTuple> {
        return this.serverInfoSubject;
    }

    get isSetup(): boolean {
        return this.serverInfo != null
            && this.serverInfo.host != null
            && this.serverInfo.hasConnected;
    }

    get isConnected(): boolean {
        return this.isSetup && this.vortexStatusService.snapshot.isOnline;
    }

    get serverHost(): string {
        return this.serverInfo.host;
    }

    get serverUseSsl(): boolean {
        return this.serverInfo.useSsl;
    }

    get serverHttpPort(): number {
        return this.serverInfo.httpPort;
    }

    get serverWebsocketPort(): number {
        return this.serverInfo.websocketPort;
    }


    /** Set Server and Port
     *
     * Set the vortex server and port, persist the information to a websqldb
     */
    setServer(serverInfo: ServerInfoTuple): Promise<void> {
        this.serverInfo = serverInfo;

        let sub = this.vortexStatusService.isOnline
            .filter(online => online == true)
            .subscribe(() => {
                this.serverInfo.hasConnected = true;
                this.saveConnInfo();
                this.balloonMsg.showSuccess("Reconnection Successful");
                sub.unsubscribe();
                this.nav.toHome();
            });

        this.updateVortex();

        // Store the data
        return this.saveConnInfo();
    }

    /** Load Conn Info
     *
     * Load the connection info from the websql db and set set the vortex.
     */
    private loadConnInfo(): Promise<void> {
        return this.tupleService.offlineStorage
            .loadTuples(this.tupleSelector)
            .then((tuples: ServerInfoTuple[]) => {
                if (tuples.length != 0) {
                    this.serverInfo = tuples[0];
                    this.serverInfoSubject.next(this.serverInfo);
                }
            });
    }

    private saveConnInfo(): Promise<void> {
        this.serverInfoSubject.next(this.serverInfo);

        // Store the data
        return this.tupleService.offlineStorage
            .saveTuples(this.tupleSelector, [this.serverInfo])
            // Convert result to void
            .then(() => Promise.resolve())
            .catch(e => {
                console.log(e);
                this.balloonMsg.showError(`Error storing server details ${e}`);
            });
    }

    private updateVortex() {
        let host = this.serverInfo.host;
        let port = this.serverInfo.websocketPort;
        let prot = this.serverInfo.useSsl ? 'wss' : 'ws';

        VortexService.setVortexUrl(`${prot}://${host}:${port}/vortexws`);
        this.vortexService.reconnect();

        this.setupOnlinePing();
    }

    /** Setup Online Ping
     *
     * This method sends a payload to the server when we detect that the vortex is
     * back online.
     *
     * The client listens for these payloads and tells the server acoordingly.
     *
     */
    private setupOnlinePing() {
        if (this.lastOnlineSub != null) {
            this.lastOnlineSub.unsubscribe();
            this.lastOnlineSub = null;
        }

        // Setup the online ping
        this.tupleService.hardwareInfo
            .uuid()
            .then(deviceId => {
                let filt = extend({deviceId: deviceId}, this.deviceOnlineFilt);

                this.lastOnlineSub = this.vortexStatusService.isOnline
                    .filter(online => online) // Filter for online only
                    .subscribe(() => {
                        this.vortexService.sendFilt(filt);
                    });

                if (this.vortexStatusService.snapshot.isOnline)
                    this.vortexService.sendFilt(filt);


            });
    }

}