# giraffe-jmxtrans #

A simple [Giraffe](http://github.com/kenhub/giraffe) configuration generator for jmxtrans metrics in Graphite (pushed via [chef-jmxtrans](http://github.com/bryanwb/chef-jmxtrans) or others).

## Usage ##

### Installation ###

* Create a "jmxtrans" Giraffe dashboard from its repository
* Save giraffe-jmxtrans.py to a useful location
* Ensure giraffe-jmxtrans.py configuration at top is correct for your environment
* Run giraffe-jmxtrans.py (or better yet setup a crontab)
* Add the following line to your Giraffe index.html below the dashboards.js line: `<script src="dashboards-jmxtrans.js"></script>`
* Comment out the `var dashboards` section of Giraffe dashboards.js

## Contributing ##

Please use standard Github issues/pull requests.

## License and Author ##
      
Author:: Brian Flad (<bflad417@gmail.com>)

Copyright:: 2013

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
