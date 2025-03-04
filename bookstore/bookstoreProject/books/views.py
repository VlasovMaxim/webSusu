from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.hashers import check_password
from .models import Book, User, Order
from django.http import HttpResponseForbidden
from .forms import BookForm, RegisterForm, LoginForm, ProfileForm
from django.core.paginator import Paginator

def book_list(request):
    books = Book.objects.all()
    paginator = Paginator(books, 3)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    user_id = request.session.get("user_id")
    user = None
    if user_id:
        user = User.objects.get(id=user_id)

    return render(request, "books/book_list.html", {"page_obj": page_obj, "user": user})

def book_create(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return HttpResponseForbidden("Только авторизованные пользователи могут добавлять книги.")

    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("book_list")
    else:
        form = BookForm()

    return render(request, "books/book_form.html", {"form": form})


def book_update(request, book_id):
    user_id = request.session.get("user_id")
    if not user_id:
        return HttpResponseForbidden("Только авторизованные пользователи могут изменять книги.")

    user = User.objects.get(id=user_id)
    if user.role != "admin":
        return HttpResponseForbidden("Только администратор может изменять книги.")

    book = Book.objects.get(id=book_id)
    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect("book_list")
    else:
        form = BookForm(instance=book)

    return render(request, "books/book_form.html", {"form": form})


def book_delete(request, book_id):
    user_id = request.session.get("user_id")
    if not user_id:
        return HttpResponseForbidden("Только авторизованные пользователи могут удалять книги.")

    user = User.objects.get(id=user_id)
    if user.role != "admin":
        return HttpResponseForbidden("Только администратор может удалять книги.")

    book = Book.objects.get(id=book_id)
    book.delete()
    return redirect("book_list")

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = RegisterForm()
    return render(request, "books/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            try:
                user = User.objects.get(username=username)
                if check_password(password, user.password):
                    request.session["user_id"] = user.id  # Сохраняем ID пользователя в сессии
                    request.session["username"] = user.username  # Можно хранить имя для отображения
                    return redirect("book_list")
                else:
                    form.add_error(None, "Неверный пароль")
            except User.DoesNotExist:
                form.add_error(None, "Пользователь не найден")
    else:
        form = LoginForm()
    return render(request, "books/login.html", {"form": form})


def logout_view(request):
    request.session.flush()  # Очистка сессии
    return redirect("login")

def profile(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect("login")  # Если не авторизован, перенаправляем на вход

    user = get_object_or_404(User, id=user_id)

    if request.method == "POST":
        form = ProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("profile")  # После сохранения перезагружаем страницу
    else:
        form = ProfileForm(instance=user)

    return render(request, "books/profile.html", {"form": form})

def add_to_cart(request, book_id):
    cart = request.session.get("cart", [])
    cart.append(book_id)
    request.session["cart"] = cart
    return redirect("cart")

def cart(request):
    cart = request.session.get("cart", [])
    books = Book.objects.filter(id__in=cart)
    total_price = sum(book.price for book in books)

    return render(request, "books/cart.html", {"books": books, "total_price": total_price})

def checkout(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect("login")

    cart = request.session.get("cart", [])
    if not cart:
        return redirect("cart")

    books = Book.objects.filter(id__in=cart)
    total_price = sum(book.price for book in books)

    order = Order.objects.create(user_id=user_id, total_price=total_price)
    order.books.set(books)
    request.session["cart"] = []  # Очищаем корзину

    return redirect("orders")

def orders(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect("login")

    orders = Order.objects.filter(user_id=user_id).order_by("-created_at")
    return render(request, "books/orders.html", {"orders": orders})

def profile(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect("login")

    user = get_object_or_404(User, id=user_id)

    if request.method == "POST":
        form = ProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("profile")
    else:
        form = ProfileForm(instance=user)

    return render(request, "books/profile.html", {"form": form})
