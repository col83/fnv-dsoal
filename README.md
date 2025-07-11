> [!NOTE]
> <h3>BUILD INFO:</h3> <p>
> DSOAL - https://github.com/kcat/dsoal/actions/runs/16158074777 <p>
> soft_oal-Win*-Release - https://github.com/kcat/openal-soft/actions/runs/16123191571 <p>
> openal-soft (utils) (x64) - https://github.com/kcat/openal-soft/actions/runs/16123191547


<h3>Introduction:</h3>

This contains files to ensure installation of surround sound for Fallout New Vegas and/or another game that USES DirectSound technology.

The principles of installation and interaction will be described below.

The necessary links to sources are left for a clearer understanding of what is happening.

<h3>EXPLANATION:</h3>

By default, Windows has a specific order for searching (loading) dynamically attached libraries (.dll)

In the case of PACKAGED applications (.exe), the system searches in the following order:

1. DLL redirection.
2. API sets.
3. Desktop apps only (not UWP apps). SxS manifest redirection.
4. Loaded-module list.
5. Known DLLs.

6. The package dependency graph of the process. This is the application's package plus any dependencies specified as <PackageDependency> in the <Dependencies> section of the application's package manifest. Dependencies are searched in the order they appear in the manifest.

7. The folder the calling process was loaded from (the executable's folder).
8. The system folder (%SystemRoot%\system32).

If a DLL has dependencies, then the system searches for the dependent DLLs as if they were loaded with just their module names (even if the first DLL was loaded by specifying a full path).

MORE INFO:

https://learn.microsoft.com/windows/win32/dlls/dynamic-link-library-search-order

https://learn.microsoft.com/windows/win32/dlls/dynamic-link-library-search-order#search-order-for-packaged-apps

<br>

> [!WARNING] <p>
> Actions to modify the registry will cause the system to load the program with other instances of the dsound.dll library instead of the built-in ones: <p>
> %SYSTEMROOT%\System32\dsound.dll (x64) <p>
> %SYSTEMROOT%\SysWOW64\dsound.dll (x32) <p>
> In simple terms, the system will simulate the actions of point 8 as point 7. As described above.

<br>

MORE INFO - https://www.indirectsound.com/registryIssues.html

This approach provides the ability to use spatial audio in games that have not fully implemented this feature or have implemented it poorly.

MORE INFO - https://www.indirectsound.com/

<br>

```
git clone https://github.com/col83/fnv-dsoal.git
```
