<p align="center">
  <img src="iAlturki_3d.svg" alt="iAlturki" />
</p>

<p align="center">
  <a href="#"><img src="https://readme-typing-svg.demolab.com?font=JetBrains+Mono&weight=500&size=18&pause=900&color=B8C0CC&center=true&vCenter=true&width=640&height=40&lines=Full-stack+web+developer+%C2%B7+systems+tinkerer;React+%C2%B7+TypeScript+%C2%B7+Node+%E2%80%94+end+to+end;C+%C2%B7+PowerShell+%E2%80%94+when+the+OS+needs+fixing;Software+that+speaks+for+itself" alt="tagline" /></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Open_to-Software_Engineering_roles-8CFF8C?style=for-the-badge&labelColor=0D1117" alt="open to work" />
  <a href="https://444005129.xyz"><img src="https://img.shields.io/badge/Portfolio-444005129.xyz-0D1117?style=for-the-badge&logo=firefoxbrowser&logoColor=8CFF8C&labelColor=0D1117" alt="Portfolio" /></a>
  <img src="https://komarev.com/ghpvc/?username=iAlturki&label=Profile+views&color=2E8B2E&style=for-the-badge" alt="profile views" />
</p>

---

### whoami

```js
const iAlturki = {
  role:     "Full-stack web developer · systems & utilities on the side",
  web:      ["React", "TypeScript", "Node / Express", "Vite"],
  systems:  ["Windows utilities", "low-level tooling", "C", "PowerShell"],
  data:     ["SQLite", "MongoDB", "SQL Server", "MariaDB"],
  building: ["MicMute", "NVIDIA Instant Replay Fix"],
  motto:    "Software that speaks for itself",
};
```

---

### Tech Stack

**Web**

<img src="https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB" /> <img src="https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white" /> <img src="https://img.shields.io/badge/Node.js-339933?style=for-the-badge&logo=nodedotjs&logoColor=white" /> <img src="https://img.shields.io/badge/Express-0D1117?style=for-the-badge&logo=express&logoColor=white" /> <img src="https://img.shields.io/badge/Vite-646CFF?style=for-the-badge&logo=vite&logoColor=white" /> <img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black" /> <img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white" /> <img src="https://img.shields.io/badge/GLSL-5586A4?style=for-the-badge&logo=opengl&logoColor=white" />

**Systems**

<img src="https://img.shields.io/badge/C-00599C?style=for-the-badge&logo=c&logoColor=white" /> <img src="https://img.shields.io/badge/PowerShell-5391FE?style=for-the-badge&logo=powershell&logoColor=white" /> <img src="https://img.shields.io/badge/Java-ED8B00?style=for-the-badge&logo=openjdk&logoColor=white" /> <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />

**Data · Tools · Platforms**

<img src="https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white" /> <img src="https://img.shields.io/badge/MongoDB-47A248?style=for-the-badge&logo=mongodb&logoColor=white" /> <img src="https://img.shields.io/badge/SQL%20Server-CC2927?style=for-the-badge&logo=microsoftsqlserver&logoColor=white" /> <img src="https://img.shields.io/badge/MariaDB-003545?style=for-the-badge&logo=mariadb&logoColor=white" /> <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" /> <img src="https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white" /> <img src="https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black" /> <img src="https://img.shields.io/badge/Photoshop-31A8FF?style=for-the-badge&logo=adobephotoshop&logoColor=white" />

---

### Code

From [MicMute](https://github.com/iAlturki/MicMute) — toggling the default microphone through the Windows Core Audio API (COM). The app tags its own changes with a private event GUID so its volume callback never reacts to itself:

```c
// audio.c - set the default mic's mute state via Core Audio (COM).
// Our own changes carry GUID_MicMuteEvent, so the volume callback ignores them.
void SetMicMute(BOOL mute)
{
    if (!g_micVol) {
        TrayBalloon(APP_NAME, L"No microphone available.");
        return;
    }
    if (SUCCEEDED(g_micVol->lpVtbl->SetMute(g_micVol, mute, &GUID_MicMuteEvent))) {
        g_appState.isMuted = mute;
        SyncMuteUI();
        PlayFeedback(mute);
    }
}

void ToggleMicrophone(void) { SetMicMute(!g_appState.isMuted); }
```

And how I like my TypeScript — failures typed, not thrown:

```ts
// result.ts — errors as values, so the compiler makes you handle them.
type Ok<T>  = { ok: true;  value: T };
type Err<E> = { ok: false; error: E };
export type Result<T, E = Error> = Ok<T> | Err<E>;

export const attempt = async <T>(fn: () => Promise<T>): Promise<Result<T>> => {
  try   { return { ok: true,  value: await fn() }; }
  catch (e) { return { ok: false, error: e instanceof Error ? e : new Error(String(e)) }; }
};
```

---

### Featured Projects

<a href="https://github.com/iAlturki/MicMute"><img src="https://github-readme-stats.vercel.app/api/pin/?username=iAlturki&repo=MicMute&hide_border=true&bg_color=00000000&title_color=8CFF8C&icon_color=76B900&text_color=C9D1D9" alt="MicMute" /></a> <a href="https://github.com/iAlturki/Nvidia_Instant_Replay_Fix"><img src="https://github-readme-stats.vercel.app/api/pin/?username=iAlturki&repo=Nvidia_Instant_Replay_Fix&hide_border=true&bg_color=00000000&title_color=8CFF8C&icon_color=76B900&text_color=C9D1D9" alt="NVIDIA Instant Replay Fix" /></a>

<p><a href="https://444005129.xyz">See the full portfolio at 444005129.xyz →</a></p>

---

### Most Used Languages

<img src="https://github-readme-stats.vercel.app/api/top-langs/?username=iAlturki&layout=compact&langs_count=8&hide_border=true&bg_color=00000000&title_color=8CFF8C&text_color=C9D1D9" alt="top languages" />

---

<p align="center"><i>Software that speaks for itself.</i></p>
