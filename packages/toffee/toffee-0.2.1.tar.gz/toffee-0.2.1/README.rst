.. Copyright 2014 Oliver Cope
..
.. Licensed under the Apache License, Version 2.0 (the "License");
.. you may not use this file except in compliance with the License.
.. You may obtain a copy of the License at
..
..     http://www.apache.org/licenses/LICENSE-2.0
..
.. Unless required by applicable law or agreed to in writing, software
.. distributed under the License is distributed on an "AS IS" BASIS,
.. WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
.. See the License for the specific language governing permissions and
.. limitations under the License.

Toffee: Test Object Factory Fixtures
====================================

Toffee creates factories for your model fixtures::

    from toffee import Fixture, Factory

    product_factory = Factory(Product, id=Seq())


    class MyFixture(Fixture):
        product_1 = product_factory(desc='cuddly toy')
        product_2 = product_factory(desc='toy tractor')
        user = Factory(User, username='fred')
        order = Factory(Order, user=user, products=[product_1, product_2])


    def test_product_search():
	with MyFixture() as f:
          assert f.product_1 in search_products('toy')
          assert f.product_2 in search_products('toy')


Toffee is similar in scope to
`factory_boy <https://github.com/dnerdy/factory_boy>`_.
The differences that prompted me to write a new library are:

- Toffee promotes working with on fixtures as groups of objects to be created
  and destroyed as a unit, rather than individual factories
- Explicit support for setup/teardown of fixtures


Read the `Toffee documentation <http://www.ollycope.com/software/toffee/>`_ to
find out more, or visit the `bitbucket repo <https://bitbucket.com/ollyc/toffee/>`_.

Toffee is developed and maintained by `Olly Cope <https://ollycope.com/>`_.
