%define lua_version %(lua -e 'print(_VERSION)' | cut -d ' ' -f 2)
%define lua_archdir %{_libdir}/lua/%{lua_version}
Name:           lua-mpack
Version:        1.0.2
Release:        1
Summary:        Implementation of MessagePack for Lua 5.1
License:        MIT
Group:          Development/Other
Url:            https://github.com/tarruda/libmpack
Source:         https://github.com/tarruda/libmpack/archive/%{version}.tar.gz
BuildRequires:  libtool
BuildRequires:  lua-devel
Requires:       lua

%description

mpack is a small binary serialization/RPC library that implements
both the msgpack and msgpack-rpc specifications.

%prep
%setup -q -n libmpack-%{version}
sed -i 's!luaL_reg!luaL_Reg!g' binding/lua/lmpack.c

%build
%{__cc} %{optflags} -I%{_includedir}/lua/%{lua_version} -shared -fPIC -o mpack.so binding/lua/lmpack.c

%install
mkdir   -p     %{buildroot}%{lua_archdir}
install -Dm755 mpack.so %{buildroot}%{lua_archdir}

%files
%doc LICENSE-MIT README.md
%dir %{lua_archdir}
%{lua_archdir}/*
