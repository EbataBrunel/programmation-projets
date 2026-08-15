import { Event } from "./Event";

export interface EventType {
    id?: number;
    publicId?: string;
    name: string;
    events?: Event[];
}
