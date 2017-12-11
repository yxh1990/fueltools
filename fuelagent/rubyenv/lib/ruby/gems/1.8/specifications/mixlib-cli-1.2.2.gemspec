# -*- encoding: utf-8 -*-

Gem::Specification.new do |s|
  s.name = %q{mixlib-cli}
  s.version = "1.2.2"

  s.required_rubygems_version = Gem::Requirement.new(">= 0") if s.respond_to? :required_rubygems_version=
  s.authors = ["Opscode, Inc."]
  s.date = %q{2011-09-08}
  s.description = %q{A simple mixin for CLI interfaces, including option parsing}
  s.email = %q{info@opscode.com}
  s.extra_rdoc_files = ["README.rdoc", "LICENSE", "NOTICE"]
  s.files = ["LICENSE", "README.rdoc", "Rakefile", "NOTICE", "lib/mixlib/cli/version.rb", "lib/mixlib/cli.rb", "spec/mixlib/cli_spec.rb", "spec/spec_helper.rb"]
  s.homepage = %q{http://www.opscode.com}
  s.require_paths = ["lib"]
  s.rubygems_version = %q{1.3.7}
  s.summary = %q{A simple mixin for CLI interfaces, including option parsing}

  if s.respond_to? :specification_version then
    current_version = Gem::Specification::CURRENT_SPECIFICATION_VERSION
    s.specification_version = 3

    if Gem::Version.new(Gem::VERSION) >= Gem::Version.new('1.2.0') then
    else
    end
  else
  end
end
