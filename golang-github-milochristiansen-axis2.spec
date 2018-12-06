%global with_devel 1
%global with_bundled 0
%global with_debug 0
%global with_check 1
%global with_unit_test 1

%if 0%{?with_debug}
%global _dwz_low_mem_die_limit 0
%else
%global debug_package   %{nil}
%endif

%global provider        github
%global provider_tld    com
%global project         milochristiansen
%global repo            axis2
# https://github.com/milochristiansen/axis2
%global provider_prefix %{provider}.%{provider_tld}/%{project}/%{repo}
%global import_path     %{provider_prefix}
%global commit          20ad74518c74a422cbc5d888d03e339d896aa5f9
%global shortcommit     %(c=%{commit}; echo ${c:0:7})

Name:           golang-%{provider}-%{project}-%{repo}
Version:        0
Release:        0.8.git%{shortcommit}%{?dist}
Summary:        A simple virtual filesystem API

# License confirmed to be zlib: https://github.com/milochristiansen/lua/issues/5
# Asked upstream to explicitly add license file: https://github.com/milochristiansen/axis2/issues/1
License:        zlib
URL:            https://%{provider_prefix}
Source0:        https://%{provider_prefix}/archive/%{commit}/%{project}-%{repo}-%{shortcommit}.tar.gz

# e.g. el6 has ppc64 arch without gcc-go, so EA tag is required
ExclusiveArch:  %{?go_arches:%{go_arches}}%{!?go_arches:%{ix86} x86_64 %{arm}}
# If go_compiler is not set to 1, there is no virtual provide. Use golang instead.
BuildRequires:  %{?go_compiler:compiler(go-compiler)}%{!?go_compiler:golang}

%description
AXIS is based on a few simple interfaces and a set of API functions that
operate on these interfaces. Clients use the provided implementations of
these interfaces (or provide their own custom implementations) to create
"data sources" that may be mounted on a "file system" and used for
OS-independent file IO.

AXIS was originally written to allow files inside of archives to be
handled with exactly the same API as used for files inside of directories,
but it has since grown to allow "logical" files and directories as well as
"multiplexing" multiple items on the same location (to, for example, make
two directories look and act like one). These properties make AXIS perfect
for handling data and configuration files for any program where flexibility
is important, the program does not need to know where its files are actually
located, it simply needs them to be at a certain place in it's AXIS file
system. Changing where a program loads it's files from is then as simple
as changing the code that initializes the file system.


%if 0%{?with_devel}
%package devel
Summary:       %{summary}
BuildArch:     noarch

Provides:      golang(%{import_path}) = %{version}-%{release}
Provides:      golang(%{import_path}/sources) = %{version}-%{release}
Provides:      golang(%{import_path}/sources/zip) = %{version}-%{release}

%description devel
%{summary}

This package contains library source intended for
building other packages which use import path with
%{import_path} prefix.
%endif

%if 0%{?with_unit_test} && 0%{?with_devel}
%package unit-test-devel
Summary:         Unit tests for %{name} package
%if 0%{?with_check}
#Here comes all BuildRequires: PACKAGE the unit tests
#in %%check section need for running
%endif

# test subpackage tests code from devel subpackage
Requires:        %{name}-devel = %{version}-%{release}

%description unit-test-devel
%{summary}

This package contains unit tests for project
providing packages with %{import_path} prefix.
%endif

%prep
%setup -q -n %{repo}-%{commit}

%build

%install
# source codes for building projects
%if 0%{?with_devel}
install -d -p %{buildroot}/%{gopath}/src/%{import_path}/
echo "%%dir %%{gopath}/src/%%{import_path}/." >> devel.file-list
# find all *.go but no *_test.go files and generate devel.file-list
for file in $(find . -iname "*.go" \! -iname "*_test.go") ; do
    echo "%%dir %%{gopath}/src/%%{import_path}/$(dirname $file)" >> devel.file-list
    install -d -p %{buildroot}/%{gopath}/src/%{import_path}/$(dirname $file)
    cp -pav $file %{buildroot}/%{gopath}/src/%{import_path}/$file
    echo "%%{gopath}/src/%%{import_path}/$file" >> devel.file-list
done
%endif

# testing files for this project
%if 0%{?with_unit_test} && 0%{?with_devel}
install -d -p %{buildroot}/%{gopath}/src/%{import_path}/
# find all *_test.go files and generate unit-test.file-list
for file in $(find . -iname "*_test.go"); do
    echo "%%dir %%{gopath}/src/%%{import_path}/$(dirname $file)" >> devel.file-list
    install -d -p %{buildroot}/%{gopath}/src/%{import_path}/$(dirname $file)
    cp -pav $file %{buildroot}/%{gopath}/src/%{import_path}/$file
    echo "%%{gopath}/src/%%{import_path}/$file" >> unit-test-devel.file-list
done
%endif

%if 0%{?with_devel}
sort -u -o devel.file-list devel.file-list
%endif

%check
%if 0%{?with_check} && 0%{?with_unit_test} && 0%{?with_devel}
%if ! 0%{?with_bundled}
export GOPATH=%{buildroot}/%{gopath}:%{gopath}
%else
export GOPATH=%{buildroot}/%{gopath}:%{gopath}
%endif

%gotest %{import_path}
%endif

#define license tag if not already defined
%{!?_licensedir:%global license %doc}

%if 0%{?with_devel}
%files devel -f devel.file-list
%doc README.md
%license LICENSE
%dir %{gopath}/src/%{provider}.%{provider_tld}/%{project}
%endif

%if 0%{?with_unit_test} && 0%{?with_devel}
%files unit-test-devel -f unit-test-devel.file-list
%doc README.md
%license LICENSE
%endif

%changelog
* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.8.git20ad745
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.7.git20ad745
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.6.git20ad745
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.5.git20ad745
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jul 10 2017 Ben Rosser <rosser.bjr@gmail.com> - 0-0.4.git20ad745
- Remove conditional around with_devel defines to actually build on EPEL > 6.

* Wed Apr 05 2017 Ben Rosser <rosser.bjr@gmail.com> - 0-0.3.git20ad745
- Updated to latest upstream release, with license file.

* Wed Mar 29 2017 Ben Rosser <rosser.bjr@gmail.com> - 0-0.2.gitb5183a8
- Clean up template golang spec file, removing Godeps path and an empty ifdef block.
- Renamed download of Source0 to include the project prefix.
- Change versioning to pre-release snapshot versions.
- Include link to upstream bug requesting a license/copying file.
- Added comment asking upstream to add license file.

* Sat Dec 31 2016 Ben Rosser <rosser.bjr@gmail.com> - 0-0.1.gitb5183a8
- First package for Fedora
