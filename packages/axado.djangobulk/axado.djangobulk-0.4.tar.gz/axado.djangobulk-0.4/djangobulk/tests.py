from django.test import TestCase
from djangobulk.models import TestModelA, TestModelDate
from djangobulk.bulk import insert_many, update_many, insert_or_update_many


class InsertTest(TestCase):
    def test_basic_insert(self):
        n = TestModelA(a="Test", b=1, c=2)

        self.assertEqual(0, TestModelA.objects.all().count())
        insert_many(TestModelA, [n])
        self.assertEqual(1, TestModelA.objects.all().count())

        n = TestModelA.objects.all()[0]
        self.assertEqual(n.a, "Test")
        self.assertEqual(n.b, 1)
        self.assertEqual(n.c, 2)

    def test_multi_insert(self):
        n = TestModelA(a="Test", b=1, c=2)
        insert_many(TestModelA, [n, n, n])
        self.assertEqual(3, TestModelA.objects.all().count())

        a = TestModelA.objects.all()[0]
        b = TestModelA.objects.all()[1]
        self.assertEqual(a.a, b.a)
        self.assertEqual(a.b, b.b)
        self.assertEqual(a.c, b.c)


class UpdateTest(TestCase):
    def test_basic_update(self):
        n = TestModelA(a="Test", b=1, c=2)
        n.save()

        n.b = 3
        n.c = 4
        update_many(TestModelA, [n])
        self.assertEqual(1, TestModelA.objects.all().count())

        n = TestModelA.objects.all()[0]
        self.assertEqual(n.a, "Test")
        self.assertEqual(n.b, 3)
        self.assertEqual(n.c, 4)

    def test_nonpk_update(self):
        n = TestModelA(a="Test", b=1, c=2)
        n.save()

        n = TestModelA(a="Updated", b=1, c=4)
        update_many(TestModelA, [n], keys=['b'])
        self.assertEqual(1, TestModelA.objects.all().count())

        n = TestModelA.objects.all()[0]
        self.assertEqual(n.a, "Updated")
        self.assertEqual(n.b, 1)
        self.assertEqual(n.c, 4)

    def test_no_update(self):
        n = TestModelA(a="Test", b=1, c=2)
        n.save()

        n.b = 3
        n.c = 4
        update_many(TestModelA, [n], keys=['c'])
        self.assertEqual(1, TestModelA.objects.all().count())

        n = TestModelA.objects.all()[0]
        self.assertEqual(n.a, "Test")
        self.assertEqual(n.b, 1)
        self.assertEqual(n.c, 2)

    def test_multi_update(self):
        set1 = [
            TestModelA(a="Test1", b=1, c=2),
            TestModelA(a="Test2", b=3, c=4),
            TestModelA(a="Test3", b=5, c=6),
            ]

        insert_many(TestModelA, set1)
        self.assertEqual(3, TestModelA.objects.all().count())

        set2 = [
            TestModelA(a="Test1", b=7, c=8),
            TestModelA(a="Test2", b=9, c=10),
            TestModelA(a="Test3", b=11, c=12),
            ]

        update_many(TestModelA, set2, keys=['a'])
        self.assertEqual(3, TestModelA.objects.all().count())

        for i in set2:
            n = TestModelA.objects.get(a=i.a)
            self.assertEqual(n.b, i.b)
            self.assertEqual(n.c, i.c)

    def test_multikey_update(self):
        set1 = [
            TestModelA(a="Test1", b=1, c=1),
            TestModelA(a="Test1", b=1, c=2),
            TestModelA(a="Test2", b=1, c=3),
            TestModelA(a="Test1", b=2, c=4),
            ]

        insert_many(TestModelA, set1)
        self.assertEqual(4, TestModelA.objects.all().count())

        set2 = [
            TestModelA(a="Test1", b=1, c=5),
            ]

        update_many(TestModelA, set2, keys=['a', 'b'])
        self.assertEqual(4, TestModelA.objects.all().count())
        self.assertEqual(2, TestModelA.objects.filter(a="Test1", b=1).count())

        for i in TestModelA.objects.filter(a="Test1", b=1):
            self.assertEqual(5, i.c)

        self.assertEqual(3, TestModelA.objects.get(a="Test2", b=1).c)
        self.assertEqual(4, TestModelA.objects.get(a="Test1", b=2).c)


class InsertUpdateTest(TestCase):
    def test_basic_insert_update(self):
        n = TestModelA(a="Test1", b=1, c=2)
        n.save()

        update_set = [
            TestModelA(a="Test1", b=5, c=5),
            TestModelA(a="Test2", b=6, c=6),
            ]

        insert_or_update_many(TestModelA, update_set, keys=['a'])
        self.assertEqual(2, TestModelA.objects.all().count())

        n = TestModelA.objects.get(a="Test1")
        self.assertEqual(n.b, 5)
        self.assertEqual(n.c, 5)

        n = TestModelA.objects.get(a="Test2")
        self.assertEqual(n.b, 6)
        self.assertEqual(n.c, 6)

    def test_multikey_insert_update(self):
        # Expected to fail in SQLite (no tuple comparison)
        set1 = [
            TestModelA(a="Test1", b=1, c=1),
            TestModelA(a="Test2", b=2, c=2),
            ]

        insert_many(TestModelA, set1)
        self.assertEqual(2, TestModelA.objects.all().count())

        set2 = [
            TestModelA(a="Test1", b=1, c=3),
            TestModelA(a="Test2", b=3, c=4),
            TestModelA(a="Test3", b=3, c=3),
            ]

        insert_or_update_many(TestModelA, set2, keys=['a', 'b'])
        self.assertEqual(4, TestModelA.objects.all().count())
        self.assertEqual(2, TestModelA.objects.filter(a="Test2").count())

        self.assertEqual(3, TestModelA.objects.get(a="Test1", b=1).c)
        self.assertEqual(3, TestModelA.objects.get(a="Test3", b=3).c)

    def test_big_insert_update(self):
        # Expected to fail in SQLite (too many variables)
        set1 = [TestModelA(a="Test", b=i, c=1) for i in range(1000)]

        insert_many(TestModelA, set1)
        self.assertEqual(1000, TestModelA.objects.all().count())

        set2 = [TestModelA(a="Test", b=i, c=2) for i in range(500, 2000)]
        insert_or_update_many(TestModelA, set2, keys=['b'])
        self.assertEqual(2000, TestModelA.objects.all().count())

    def test_duplicate_insert_update(self):
        set1 = [
            TestModelA(a="Test1", b=1, c=1),
            TestModelA(a="Test2", b=2, c=2),
            TestModelA(a="Test2", b=2, c=3),
            ]

        insert_or_update_many(TestModelA, set1, keys=['b'])
        self.assertEqual(2, TestModelA.objects.all().count())
        self.assertEqual(3, TestModelA.objects.get(a="Test2").c)


class UpdateDateTimeTest(TestCase):
    def test_insert_must_set_the_date(self):
        obj = TestModelDate()

        insert_many(TestModelDate, [obj])

        obj = TestModelDate.objects.all()[0]
        assert obj.created
        assert obj.updated

    def test_update_must_not_update_auto_now_add(self):
        obj = TestModelDate()
        obj.save()
        created = obj.created
        updated = obj.updated

        update_many(TestModelDate, [obj])

        obj = TestModelDate.objects.all()[0]
        assert obj.created == created, 'Created (auto_now_add=True) must not change'
        assert obj.updated != updated, 'Updated (auto_now=True) must change'

    def test_update_must_set_the_date(self):
        obj = TestModelDate()
        obj.save()
        created = obj.created
        updated = obj.updated

        insert_or_update_many(TestModelDate, [obj, TestModelDate()])

        obj = TestModelDate.objects.filter(pk=obj.pk)[0]
        assert obj.created == created, 'Created (auto_now_add=True) must not change'
        assert obj.updated != updated, 'Updated (auto_now=True) must change'

        obj = TestModelDate.objects.exclude(pk=obj.pk)[0]
        assert obj.created
        assert obj.updated
