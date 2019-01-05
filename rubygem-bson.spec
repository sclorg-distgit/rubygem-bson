%{?scl:%scl_package rubygem-%{gem_name}}
%{!?scl:%global pkg_name %{name}}

# Enable test when building on local.
%bcond_with tests

# Generated from bson-1.3.1.gem by gem2rpm -*- rpm-spec -*-
%global gem_name bson

Name: %{?scl_prefix}rubygem-%{gem_name}
Version: 4.3.0
Release: 1.bs1%{?dist}
Summary: Ruby Implementation of the BSON specification
Group: Development/Languages
License: ASL 2.0
URL: http://bsonspec.org
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# Sources for rspec to test internally.
# Enable lines of Source code when testing on local. Don't import those.
# Source200: diff-lcs-1.3.gem
# Source201: rspec-3.7.0.gem
# Source202: rspec-core-3.7.0.gem
# Source203: rspec-expectations-3.7.0.gem
# Source204: rspec-mocks-3.7.0.gem
# Source205: rspec-support-3.7.0.gem

Requires: %{?scl_prefix}rubygem(bigdecimal)
Requires:      %{?scl_prefix}ruby(release)
Requires:      %{?scl_prefix}ruby(rubygems) >= 1.3.6
BuildRequires: %{?scl_prefix}ruby(release)
BuildRequires: %{?scl_prefix}ruby(rubygems)
BuildRequires: %{?scl_prefix}ruby-devel >= 1.9.3
BuildRequires: %{?scl_prefix}rubygems-devel >= 1.3.6
BuildRequires: %{?scl_prefix}rubygem(bigdecimal)
Provides:      %{?scl_prefix}rubygem(%{gem_name}) = %{version}
# This package contains the binary extension originaly provided by bson_ext
# since F26 timeframe.
Provides: rubygem-bson_ext%{?_isa} = %{version}-%{release}
Provides: rubygem-bson_ext = %{version}-%{release}
Provides: rubygem(bson_ext) = %{version}-%{release}
Obsoletes: rubygem-bson_ext < 4.1.1-1

%description
A full featured BSON specification implementation, in Ruby.

%package doc
Summary: Documentation for %{pkg_name}
Group: Documentation
Requires:%{?scl_prefix}%{pkg_name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{pkg_name}.

%prep
%{?scl:scl enable %{scl} - << \EOF}
set -ex
gem unpack %{SOURCE0}

%setup -q -D -T -n  %{gem_name}-%{version}

gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec
%{?scl:EOF}

%build
%{?scl:scl enable %{scl} - << \EOF}
set -ex
gem build %{gem_name}.gemspec
%gem_install
%{?scl:EOF}

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

mkdir -p %{buildroot}%{gem_extdir_mri}/
cp -a .%{gem_extdir_mri}/{gem.build_complete,*.so} %{buildroot}%{gem_extdir_mri}/

# Prevent dangling symlink in -debuginfo (rhbz#878863).
# Directory currently nonexistent.
rm -rf %{buildroot}%{gem_instdir}/ext/

%if %{with tests}
%check
%{?scl:scl enable %{scl} - << \EOF}
set -ex
pushd .%{gem_instdir}

# mkdir gems
# pushd gems
# cp -p "%%{SOURCE200}" .
# cp -p "%%{SOURCE201}" .
# cp -p "%%{SOURCE202}" .
# cp -p "%%{SOURCE203}" .
# cp -p "%%{SOURCE204}" .
# cp -p "%%{SOURCE205}" .
# gem install *.gem --local --no-document
# # Path to rspec is not set in Copr.
# export PATH="~/bin:${PATH}"
# popd

rspec -I$(dirs +1)%{gem_extdir_mri}:lib spec
popd
%{?scl:EOF}
%endif

%files
%dir %{gem_instdir}
%{gem_extdir_mri}
%license %{gem_instdir}/LICENSE
%{gem_instdir}/NOTICE
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CHANGELOG.md
%doc %{gem_instdir}/CONTRIBUTING.md
%doc %{gem_instdir}/README.md
%{gem_instdir}/Rakefile
%{gem_instdir}/spec

%changelog
* Fri Feb 16 2018 Jun Aruga <jaruga@redhat.com> - 4.3.0-1
- Update to bson 4.3.0.
- Remove Obsoletes (rhbz#1537219)

* Fri Jan 05 2018 Jun Aruga <jaruga@redhat.com> - 4.2.2-2
- Update to bson 4.2.2.

* Tue Feb 14 2017 Jun Aruga <jaruga@redhat.com> - 4.2.1-2
- Fix Fixnum/Bignum deprecated warning for Ruby 2.4.0.

* Thu Jan 19 2017 Jun Aruga <jaruga@redhat.com> - 4.2.1-1
- Update to bson 4.2.1.
- Add BigDecimal dependnecy.
- Fix build on PPC.

* Wed Apr 06 2016 Pavel Valena <pvalena@redhat.com> - 4.0.3-2
- Fix: build should fail on test failure

* Mon Feb 29 2016 Pavel Valena <pvalena@redhat.com> - 4.0.3-1
- Update to 4.0.3

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 26 2014 Vít Ondruch <vondruch@redhat.com> - 1.10.2-1
- Update to bson 1.10.2.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Nov 19 2013 Vít Ondruch <vondruch@redhat.com> - 1.9.2-1
- Update to bson 1.9.2.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Mar 06 2013 Vít Ondruch <vondruch@redhat.com> - 1.6.4-3
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Aug 08 2012 Vít Ondruch <vondruch@redhat.com> - 1.6.4-1
- Update to bson 1.6.4.

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Feb 02 2012 Vít Ondruch <vondruch@redhat.com> - 1.4.0-3
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Sep 22 2011 Vít Ondruch <vondruch@redhat.com> - 1.4.0-1
- Update to bson 1.4.0

* Wed May 25 2011 Vít Ondruch <vondruch@redhat.com> - 1.3.1-1
- Initial package
