<a href="https://444005129.xyz"><picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/banner-dark.svg">
  <img src="assets/banner-light.svg" width="846" alt="iAlturki, each letter drawn out of small copies of itself. Beside it, MicMute's mute badge plays its real timeline once: it fades in, its plate melts away after 3 seconds, and the slashed microphone settles at 70% opacity.">
</picture></a>

**iAlturki.** Software engineer. I build small native Windows tools in plain C, plus web work.
Open to software engineering roles: **[open a hiring inquiry](https://github.com/iAlturki/iAlturki/issues/new?template=hire.yml)**, a short public issue form. I reply in the thread. Site: [444005129.xyz](https://444005129.xyz)

| Tool | What it does | Latest release |
|:--|:--|:--|
| **[MicMute](https://github.com/iAlturki/MicMute)** | A global hotkey (<kbd>F8</kbd> by default) mutes your default Windows microphone and shows a click-through badge on every monitor. Event-driven Core Audio through COM interfaces implemented in plain C. | <!-- tag:MicMute -->v2.1.2<!-- /tag -->, <!-- size:MicMute -->159,232<!-- /size --> bytes |
| **[Instant Replay Fix](https://github.com/iAlturki/Nvidia_Instant_Replay_Fix)** | Keeps NVIDIA's Instant Replay recording when an app NVIDIA treats as protected is on screen. Finds NVIDIA's decision code by the log strings it ships, so it survives updates. | <!-- tag:Nvidia_Instant_Replay_Fix -->v1.0.2<!-- /tag -->, <!-- size:Nvidia_Instant_Replay_Fix -->233,984<!-- /size --> bytes |
| **[Look20](https://github.com/iAlturki/Look20)** | Every 20 minutes of active use, a pixel-art eye bubble slides onto every monitor for a 20-second break. Clicks pass through it. | <!-- tag:Look20 -->v1.0.0<!-- /tag -->, <!-- size:Look20 -->172,032<!-- /size --> bytes |

MicMute's releases have been downloaded <!-- dl:MicMute -->263<!-- /dl --> times and Instant Replay Fix's <!-- dl:Nvidia_Instant_Replay_Fix -->170<!-- /dl --> times <sub>(GitHub Releases API, every asset and repeat download counted, as of <!-- asof -->1 October 2026<!-- /asof -->; refreshed by [a workflow](.github/workflows/releases.yml))</sub>.

### Notes from the work

- **MicMute never reacts to its own writes.** Every write carries a private event-context GUID, and the Core Audio callback drops it before anything crosses threads. [`audio.c`, lines 37 to 47](https://github.com/iAlturki/MicMute/blob/9a054c4e7bc8413cf76cac2093fd71ef5e03c3bc/src/audio.c#L37-L47)
- **Look20's bubble grew from 585 to 731 px mid-slide**, because `WM_DPICHANGED` scaled an already-scaled window at the monitor seam. It is now honoured only while the bubble rests. Caught before release. [`main.c`, lines 1110 to 1126](https://github.com/iAlturki/Look20/blob/ba739ef879be90836b76e51dc25cbf4401afd404/main.c#L1110-L1126)
- **MicMute crashed at logon, for two different reasons.** Tray creation is now never fatal and retries until Explorer is up ([`6542784`](https://github.com/iAlturki/MicMute/commit/654278487b785d985951965795911b82ab9409ae)), and every launch re-points the autostart task at the running .exe ([`9a054c4`](https://github.com/iAlturki/MicMute/commit/9a054c4e7bc8413cf76cac2093fd71ef5e03c3bc)).
- **NVIDIA has no off switch for the branch that stops Instant Replay.** After 16 reconnaissance surfaces ([write-up](https://github.com/iAlturki/Nvidia_Instant_Replay_Fix/blob/bcbe079c88b800c9859147c06e4a896adac0ecb1/c/PERSISTENT_OFFSWITCH.md)), the fix watches NVIDIA's registry key instead. Based on the approach pioneered by [furyzenblade/ShadowPlay_Patcher](https://github.com/furyzenblade/ShadowPlay_Patcher); independent reimplementation, unofficial, not affiliated with NVIDIA.
- **Windows Defender's ML flagged Look20's MinGW build.** Releases now build with MSVC and a static CRT (`/MT`). [`988f00e`](https://github.com/iAlturki/Look20/commit/988f00e739dc33a556d095bfc69f773160e0d665)

<details>
<summary><b>Read 11 lines of MicMute:</b> <code>src/audio.c</code>, lines 37 to 47</summary>

```c
static HRESULT STDMETHODCALLTYPE VC_OnNotify(IAudioEndpointVolumeCallback* This, PAUDIO_VOLUME_NOTIFICATION_DATA n)
{
    if (!n) return E_POINTER;
    if (IsEqualGUID(&n->guidEventContext, &GUID_MicMuteEvent)) return S_OK;
    // marshal to the UI thread
    PostMessageW(g_appState.hWnd, WM_APP_AUDIO, (WPARAM)n->bMuted, (LPARAM)(int)(n->fMasterVolume * 10000.0f));
    return S_OK;
}

static IAudioEndpointVolumeCallbackVtbl g_volCbVtbl = {VC_QueryInterface, VC_AddRef, VC_Release, VC_OnNotify};
static IAudioEndpointVolumeCallback g_volCb = {&g_volCbVtbl};
```

VC_OnNotify runs on a Core Audio thread. It drops events tagged with MicMute's own GUID and posts everything else to the UI thread, where all state lives, so there are no locks. The last two lines are a COM interface built by hand in C.
</details>

<sub>Software that speaks for itself: at [444005129.xyz](https://444005129.xyz), MicMute's overlay runs in your browser. Press <kbd>F8</kbd>.</sub>
