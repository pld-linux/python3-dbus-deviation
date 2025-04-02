#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests

Summary:	Parse D-Bus introspection XML and process it in varous ways
Summary(pl.UTF-8):	Analiza opisów XML protokołu D-Bus i przetwarzanie na różne sposoby
Name:		python3-dbus-deviation
Version:	0.6.1
Release:	3
License:	LGPL v2.1+
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/dbus-deviation/
Source0:	https://files.pythonhosted.org/packages/source/d/dbus-deviation/dbus-deviation-%{version}.tar.gz
# Source0-md5:	649e1024a024242bfc38a5e1dfec69b4
Patch0:		dbus-deviation-tests.patch
URL:		https://pypi.org/project/dbus-deviation/
BuildRequires:	python3-Sphinx
BuildRequires:	python3-modules >= 1:3.2
BuildRequires:	python3-setuptools
BuildRequires:	python3-setuptools_git >= 0.3
%if %{with tests}
BuildRequires:	python3-lxml
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python3-modules >= 1:3.2
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
dbus-deviation is a project for parsing D-Bus introspection XML and
processing it in various ways. Its main tool is dbus-interface-diff,
which calculates the difference between two D-Bus APIs for the purpose
of checking for API breaks.

This functionality is also available as a Python module,
dbusdeviation.

%description -l pl.UTF-8
dbus-deviation to projekt do analizy opisów XML protokołu D-Bus i
przetwarzania ich na różne sposoby. Główne narzędzie to
dbus-interface-diff, wyliczające różnice między dwoma API D-Bus na
potrzeby sprawdzania zmian API.

Funkcjonalność jest dostępna także jako moduł Pythona dbusdeviation.

%package apidocs
Summary:	API documentation for Python dbus-deviation module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona dbus-deviation
Group:		Documentation

%description apidocs
API documentation for Python dbus-deviation module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona dbus-deviation.

%prep
%setup -q -n dbus-deviation-%{version}
%patch -P0 -p1

%build
%py3_build

%if %{with tests}
%{__python3} -m unittest discover -s dbusapi
%{__python3} -m unittest discover -s dbusdeviation
%endif

%if %{with doc}
PYTHONPATH=$(pwd) \
sphinx-build-3 -b html docs docs/build/html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%{__rm} -r $RPM_BUILD_ROOT%{py3_sitescriptdir}/{dbusapi,dbusdeviation}/tests

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS NEWS README.md
%attr(755,root,root) %{_bindir}/dbus-interface-diff
%attr(755,root,root) %{_bindir}/dbus-interface-vcs-helper
%{py3_sitescriptdir}/dbusapi
%{py3_sitescriptdir}/dbusdeviation
%{py3_sitescriptdir}/dbus_deviation-%{version}-py*.egg-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/build/html/{_modules,_static,*.html,*.js}
%endif
