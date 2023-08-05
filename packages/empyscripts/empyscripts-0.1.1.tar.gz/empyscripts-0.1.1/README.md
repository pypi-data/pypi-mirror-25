# empyscripts

This repo contains *add-ons* for `empymod`. These are scripts that did not make
it into `empymod`. Most likely because they require some sort of change to the
`empymod` core features, but are only for a very specific use cases. Hence it
was decided to not implement them in `empymod`.

Please note that these add-ons are not as thoroughly tested as `empymod`, and
potentially not as well documented either. There are, as of now, also no tests
for it.


## More information

For information regarding `empymod` have a look at:
[empymod.github.io](https://empymod.github.io).


## Installation

You can install empyscripts via `conda`

```bash
conda install -c prisae empyscripts
```

via `pip`:

```bash
pip install empyscripts
```

or download this repo and run

```bash
python setup.py install
```


## Add-ons

So far, there is only one add-on.

- `tmtemod.py`: Return up- and down-going TM/TE-mode contributions for
  x-directed electric sources and receivers, which are located in the same
  layer.


## License

Copyright 2017 Dieter Werthmüller

Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this file except in compliance with the License.  You may obtain a copy of the
License at

[http://www.apache.org/licenses/LICENSE-2.0](http://www.apache.org/licenses/LICENSE-2.0)

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied.  See the License for the
specific language governing permissions and limitations under the License.

See the *LICENSE*-file in the root directory for a full reprint of the Apache
License.
