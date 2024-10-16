import type { ToastSettings } from "@skeletonlabs/skeleton";

export function MakeToastMessage(
    message: string,
    type: 'success' | 'error' | 'info' | 'warning' = 'info',
    timeout?: number // Optional: timeout in milliseconds
): ToastSettings {
    let settings: ToastSettings = {
        message,
        background: `variant-filled-${type}`
    }
    if (timeout !== undefined) {
        settings.timeout = timeout;
    }
    return settings;
}
