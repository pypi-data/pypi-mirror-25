Copyright (c) 2017 Joakim Uddholm

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Description: badger
        ======
        |version| |coverage|
        
        Commandline Interface to create svg badges.
        
        Install
        -------
        
        .. code:: bash
        
            pip install badger
        
        Usage (Commandline)
        -------------------
        
        Simplest use case of static label and value:
        
        .. code:: bash      
        
            badger version v0.1.1
        
        Percentage mode, with color picked relative to where in the 0-100 range
        the value is.
        
        .. code:: bash
        
            badger -p coverage 71.29%
        
        
        Usage (Package)
        ---------------
        
        .. code:: python
        
            from badger import Badge, PercentageBadge
        
            badge = Badge("version", "v0.1.1")
            badge.save("examples/version.svg")
        
            percentage_badge = PercentageBadge("coverage", 71.29)
            badge.save("examples/coverage.svg")
        
        Disclaimer
        ==========
        
        Code originally heavily copied from https://github.com/dbrgn/coverage-badge . Badge
        design originally from https://github.com/badges/shields
        
        .. |version| image:: examples/version.svg
        .. |coverage| image:: examples/coverage.svg
            
        
        
Platform: UNKNOWN
Classifier: Development Status :: 3 - Alpha
Classifier: Environment :: Console
Classifier: Intended Audience :: Developers
Classifier: License :: OSI Approved :: MIT
Classifier: Programming Language :: Python :: 3
Classifier: Programming Language :: Python :: 3.3
Classifier: Programming Language :: Python :: 3.4
Classifier: Programming Language :: Python :: 3.5
Classifier: Programming Language :: Python
