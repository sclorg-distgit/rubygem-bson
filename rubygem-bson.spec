%{!?scl:%global pkg_name %{name}}
%{?scl:%scl_package rubygem-%{gem_name}}
%global gem_name bson

Summary: Ruby implementation of BSON
Name: %{?scl:%scl_prefix}rubygem-%{gem_name}
Version: 1.10.2
Release: 1%{?dist}
Group: Development/Languages
License: ASL 2.0 
URL: http://www.mongodb.org
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem
# git clone https://github.com/mongodb/mongo-ruby-driver.git && cd mongo-ruby-driver && git checkout 1.10.2
# tar czvf bson-1.10.2-tests.tgz test/bson
Source1: %{gem_name}-%{version}-tests.tgz
# Use old test_helper.rb, which does not have unnecessary dependencies.
Source2: https://raw.github.com/mongodb/mongo-ruby-driver/ffc598c0952a37fe81e35fe52e8aa0ce695cb1dd/test/bson/test_helper.rb
Requires: %{?scl_prefix_ruby}ruby(release)
Requires: %{?scl_prefix_ruby}ruby(rubygems)
BuildRequires: %{?scl_prefix_ruby}ruby(release)
BuildRequires: %{?scl_prefix_ruby}rubygems-devel
BuildRequires: %{?scl_prefix}rubygem(activesupport)
BuildRequires: %{?scl_prefix_ruby}rubygem(power_assert)
BuildRequires: %{?scl_prefix_ruby}rubygem(test-unit)
BuildArch: noarch
Provides: %{?scl_prefix}rubygem(%{gem_name}) = %{version}

%description
A Ruby BSON implementation for MongoDB. For more information about Mongo, see
http://www.mongodb.org. For more information on BSON, see
http://www.bsonspec.org.


%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}

%description doc
Documentation for %{name}


%prep
%setup -n %{pkg_name}-%{version} -q -c -T
mkdir -p .%{gem_dir}

%{?scl:scl enable %scl - << \EOF}
%gem_install -n %{SOURCE0}
%{?scl:EOF}

%build

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

mkdir -p %{buildroot}%{_bindir}
cp -a .%{_bindir}/* \
        %{buildroot}%{_bindir}/

find %{buildroot}%{gem_instdir}/bin -type f | xargs chmod a+x

%check
pushd .%{gem_instdir}
# Extract tests.
tar xzf %{SOURCE1}

# Move test_helper.rb into place.
cp %{SOURCE2} test/bson

# String#to_bson_code is implemented in Mongo.
sed -i -r "s|('this.c.d < this.e')\.to_bson_code|BSON::Code.new\(\1\)|" test/bson/bson_test.rb

%{?scl:scl enable %{scl} - << \EOF}
# StringIO is required by BSONTest#test_read_bson_document, but there is no
# point to report it upstream, since upstream switched to RSpec meanwhile.
ruby -Ilib:test/bson -e 'gem "test-unit"; Dir.glob "./test/**/*_test.rb", &method(:require)'
%{?scl:EOF}
popd

%files
%dir %{gem_instdir}
%{_bindir}/b2json
%{_bindir}/j2bson
%{gem_instdir}/LICENSE
%{gem_instdir}/VERSION
%{gem_instdir}/bin
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%{gem_instdir}/bson.gemspec


%changelog
* Thu Jun 26 2014 Vít Ondruch <vondruch@redhat.com> - 1.10.2-1
- Update to bson 1.10.2.

* Fri Mar 21 2014 Vít Ondruch <vondruch@redhat.com> - 1.9.2-2
- Rebuid against new scl-utils to depend on -runtime package.
  Resolves: rhbz#1069109

* Tue Nov 19 2013 Vít Ondruch <vondruch@redhat.com> - 1.9.2-1
- Update to bson 1.9.2.
- Import into ruby193 SCL.
  - Resolves: rhbz#1032922

* Tue Sep 03 2013 Troy Dawson <tdawson@redhat.com> - 1.9.1-1
- Updated to version 1.9.1

* Mon Jan 14 2013 Troy Dawson <tdawson@redhat.com> - 1.8.1-1
- Updated to version 1.8.1

* Thu Nov 08 2012 Troy Dawson <tdawson@redhat.com>  - 1.7.0-3
- Packaged to work with SCL

* Tue Oct 09 2012 Troy Dawson <tdawson@redhat.com> - 1.7.0-1
- Updated to version 1.7.0

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
