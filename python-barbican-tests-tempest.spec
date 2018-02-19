%{!?upstream_version: %global upstream_version %{commit}}
%global commit b79d2ea64a271436a7a29f23f26464ae0686de73
%global shortcommit %(c=%{commit}; echo ${c:0:7})
# DO NOT REMOVE ALPHATAG
%global alphatag .%{shortcommit}git

%global service barbican
%global plugin barbican-tempest-plugin
%global module barbican_tempest_plugin
# Disabling doc as it is not available
%global with_doc 0

%if 0%{?fedora}
%global with_python3 1
%endif

%if 0%{?dlrn}
%define tarsources %module
%else
%define tarsources %plugin
%endif

%global common_desc \
This project defines a tempest plugin containing tests used to verify the \
functionality of a barbican installation. The plugin will automatically load \
these tests into tempest.


Name:       python-%{service}-tests-tempest
Version:    0.0.1
Release:    0.1%{?alphatag}%{?dist}
Summary:    Tempest plugin for the barbican project.
License:    ASL 2.0
URL:        https://git.openstack.org/cgit/openstack/%{plugin}/

Source0:    https://github.com/openstack/%{plugin}/archive/%{commit}.tar.gz#/%{plugin}-%{shortcommit}.tar.gz

BuildArch:  noarch
BuildRequires:  git
BuildRequires:  openstack-macros

%description
%{common_desc}

%package -n python2-%{service}-tests-tempest
Summary: %{summary}
%{?python_provide:%python_provide python2-%{service}-tests-tempest}
BuildRequires:  python2-devel
BuildRequires:  python2-pbr
BuildRequires:  python2-setuptools

Requires:   python2-tempest >= 1:17.2.0
Requires:   python2-pbr >= 2.0.0
Requires:   python2-cryptography
Requires:   python2-oslo-config >= 2:4.0.0
Requires:   python2-oslo-log >= 3.30.0
Requires:   python2-six >= 1.9.0

%description -n python2-%{service}-tests-tempest
%{common_desc}

%if 0%{?with_doc}
%package -n python-%{service}-tests-tempest-doc
Summary:        python-%{service}-tests-tempest documentation

BuildRequires:  python2-sphinx
BuildRequires:  python2-oslo-sphinx

%description -n python-%{service}-tests-tempest-doc
It contains the documentation for the Barbican tempest tests.
%endif

%if 0%{?with_python3}
%package -n python3-%{service}-tests-tempest
Summary: %{summary}
%{?python_provide:%python_provide python3-%{service}-tests-tempest}
BuildRequires:  python3-devel
BuildRequires:  python3-pbr
BuildRequires:  python3-setuptools

Requires:   python3-tempest >= 1:17.2.0
Requires:   python3-pbr >= 2.0.0
Requires:   python3-cryptography
Requires:   python3-oslo-config >= 2:4.0.0
Requires:   python3-oslo-log >= 3.30.0
Requires:   python3-six >= 1.9.0

%description -n python3-%{service}-tests-tempest
%{common_desc}
%endif

%prep
%autosetup -n %{tarsources}-%{upstream_version} -S git

# Let's handle dependencies ourseleves
%py_req_cleanup
# Remove bundled egg-ingo
rm -rf %{module}.egg-info

%build
%if 0%{?with_python3}
%py3_build
%endif
%py2_build

# Generate Docs
%if 0%{?with_doc}
%{__python2} setup.py build_sphinx
# remove the sphinx build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%if 0%{?with_python3}
%py3_install
%endif
%py2_install

%files -n python2-%{service}-tests-tempest
%license LICENSE
%doc README.rst
%{python2_sitelib}/%{module}
%{python2_sitelib}/*.egg-info

%if 0%{?with_python3}
%files -n python3-%{service}-tests-tempest
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{module}
%{python3_sitelib}/*.egg-info
%endif

%if 0%{?with_doc}
%files -n python-%{service}-tests-tempest-doc
%doc doc/build/html
%license LICENSE
%endif

%changelog
* Mon Feb 19 2017 Chandan Kumar <chkumar@redhat.com> 0.0.1-0.1.b79d2ea6git
- Update to pre-release 0.0.1 (b79d2ea64a271436a7a29f23f26464ae0686de73)
