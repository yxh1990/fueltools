# -*- encoding: utf-8 -*-

Gem::Specification.new do |s|
  s.name = %q{cstruct}
  s.version = "1.0.1"

  s.required_rubygems_version = Gem::Requirement.new(">= 0") if s.respond_to? :required_rubygems_version=
  s.authors = ["skandhas"]
  s.date = %q{2012-02-12 00:00:00.000000000Z}
  s.email = %q{skandhas@163.com}
  s.files = ["lib/cstruct/cstruct.rb", "lib/cstruct/field.rb", "lib/cstruct/utils.rb", "lib/cstruct/win32struct.rb", "lib/cstruct/win64struct.rb", "lib/cstruct.rb", "lib/win32struct.rb", "lib/win64struct.rb", "spec/cstruct_spec.rb", "examples/anonymous_struct.rb", "examples/anonymous_union.rb", "examples/array_member.rb", "examples/file_io.rb", "examples/first_example.rb", "examples/inner_struct.rb", "examples/inner_union.rb", "examples/namespace.rb", "examples/struct_member.rb", "examples/win32/get_system_info.rb", "examples/win32/get_versionex.rb", "examples/win32/global_memory.rb", "examples/win32/show_processes.rb", "doc/documents.html", "doc/examples/anonymous_struct.rb.html", "doc/examples/anonymous_union.rb.html", "doc/examples/array_member.rb.html", "doc/examples/file_io.rb.html", "doc/examples/first_example.rb.html", "doc/examples/get_system_info.rb.html", "doc/examples/get_versionex.rb.html", "doc/examples/global_memory.rb.html", "doc/examples/inner_struct.rb.html", "doc/examples/inner_union.rb.html", "doc/examples/namespace.rb.html", "doc/examples/show_processes.rb.html", "doc/examples/struct_member.rb.html", "doc/examples.html", "doc/images/examples.png", "doc/images/excample1.png", "doc/images/excample2.png", "doc/images/green-point.png", "doc/images/learnmore.png", "doc/images/logo.png", "doc/images/news.png", "doc/images/point.png", "doc/images/start.png", "doc/images/synopsish.png", "doc/images/Thumbs.db", "doc/index.html", "doc/stylesheets/coderay.css", "doc/stylesheets/ie.css", "doc/stylesheets/style.css", "README.md", "cstruct.gemspec"]
  s.homepage = %q{http://github.com/skandhas/cstruct}
  s.require_paths = ["lib"]
  s.rubygems_version = %q{1.3.7}
  s.summary = %q{CStruct is a simulation of the C language's struct.}

  if s.respond_to? :specification_version then
    current_version = Gem::Specification::CURRENT_SPECIFICATION_VERSION
    s.specification_version = 3

    if Gem::Version.new(Gem::VERSION) >= Gem::Version.new('1.2.0') then
    else
    end
  else
  end
end
