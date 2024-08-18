
# MetaLeak: Assessing Image Metadata Leakage Through Side-Channel in Android Apps
## 1. Citation
If you use MetaLeak results, please cite the following information. Thank you.
## 2. Introduction
This is the source code of the research **"MetaLeak: Assessing Image Metadata Leakage Through Side-Channel in Android Apps"** project.

The **MetaLeak** system is used to investigate whether Android apps send sensitive metadata when users share/send/upload their image to the Internet by using Hybrid analysis.

Threat model illustrated as figure below
<img src="https://github.com/research-mobile-security/MetaLeak/blob/main/project-image/threat-model-2.png">

## 3. System architecture

**MetaLeak** is a 100% software solution aiming to leverage the Android Virtual Device (AVD) instead of physical phones to enhance flexibility and reduce costs. However, our approach also supports real devices.

MetaLeak consists of four components, as illustrated in the Figure below, including:

- **Part 1**: apps download.
- **Part 2**: static analysis. 
- **Part 3**: dynamic analysis. 
- **Part 4**: privacy compliance check. 

<img src="https://github.com/research-mobile-security/MetaLeak/blob/main/project-image/system-overview.png">


## 4. Source code

### 4.1. Souce code for Root AVD

See detailed source code and step-by-step instructions at [MetaLeak-Root-AVD](/MetaLeak-Root-AVD).

### 4.2. Souce code for Part-1: Apps Download

See detailed source code and step-by-step instructions at [MetaLeak-Apps-Download](/MetaLeak-Apps-Download).

### 4.3. Souce code for Part-2: Static Analysis

See detailed source code and step-by-step instructions at [MetaLeak-Static-Analysis](/MetaLeak-Static-Analysis).

### 4.4. Souce code for Part-3: Dynamic Analysis

See detailed source code and step-by-step instructions at:
 - Module Client-Service at [MetaLeak-Client-Service](/MetaLeak-Client-Service).
 - Module Server-Service at [MetaLeak-Server-Service](/MetaLeak-Server-Service).
 - Module Google Drive AutoDownload at [MetaLeak-Google-Drive-Auto-Download](/MetaLeak-Google-Drive-Auto-Download).
 - Module Frida-Objection for bypass SSL-pinning at  [MetaLeak-Frida-Objection](/MetaLeak-Frida-Objection).

### 4.5. Souce code for Part-4: Privacy Compliance Check 

See detailed source code and step-by-step instructions at [MetaLeak-Privacy-Compliance](/MetaLeak-Privacy-Compliance).

## 5. Video

- Please see the entire system demo at the link: https://youtu.be/Xj_IluWAnMw.
- Other instructional videos:
    - Root Android Virtual Device (AVD) on Ubuntu: https://youtu.be/feTJm_ykjYQ
    - Root Android Virtual Device (AVD) on Windows: https://youtu.be/rUCk2TM58Z0
    - Install MITM Proxy Certificate to Android Trust Credentials: https://youtu.be/P123VhRQX7s