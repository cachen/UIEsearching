#
# spec file for package UIEsearching (Version 0.1)
#
# Please submit bugfixes or comments via http://bugs.opensuse.org/

Name:           UIEsearching
License:        GNU General Public License (GPL)
Group:          SuSE internal
Summary:        Accessible information searching tool for UI Automation
Provides:	UIEsearching
Obsoletes:	UIEsearching
Requires:       strongwind
Version:        0.1
Release:        1
Source0:        %name-%version.tar.bz2
Source1:        Esearching.py
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArch:      noarch

%description
Accessible information searching tool for UI Automation test

%prep
%setup -q -n %{name}

%build

%install
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/tools
install -m 755 %{S:1} $RPM_BUILD_ROOT/usr/share/qa/tools

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
/usr/share/qa/tools

%changelog
* Thu Sep 29 2011 - cachen@suse.com
- Create the first version
