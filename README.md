<h3>BUILD INFO:</h3>

DSOAL (NO HRTF) (x32) - https://github.com/kcat/dsoal/actions/runs/15721639503

soft_oal.dll (x32) - https://github.com/kcat/openal-soft/actions/runs/15681911533

openal soft - https://github.com/kcat/openal-soft/actions/runs/15649631255


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


Registry modification actions will cause the system to load a program with a different instance of dsound.dll for the dsound.dll library than the built-in ones:

%SYSTEMROOT%\System32\dsound.dll (x64) <br>
%SYSTEMROOT%\SysWOW64\dsound.dll (x32)

Simply put - the system will imitate the actions of the 8th point of the order as the 7th point. As described above.

MORE INFO - https://www.indirectsound.com/registryIssues.html


This approach provides the ability to use spatial audio in games that have not fully implemented this feature or have implemented it poorly.

MORE INFO - https://www.indirectsound.com/

<br>

To load from scripts (in case you need it):


```
curl -fJL -# --ssl-no-revoke -o ".\fnv-dsoal.zip" https://github.com/col83/fnv-dsoal/archive/refs/heads/master.zip
```
