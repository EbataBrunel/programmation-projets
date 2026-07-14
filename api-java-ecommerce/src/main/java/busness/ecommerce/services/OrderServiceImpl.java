package busness.ecommerce.services;

import busness.ecommerce.dto.OrderItemResponseDto;
import busness.ecommerce.dto.OrderResponseDto;
import busness.ecommerce.dto.OrdersByMonthDto;
import busness.ecommerce.dto.OrdersByYearDto;
import busness.ecommerce.entity.*;
import busness.ecommerce.enums.OrderStatus;
import busness.ecommerce.mapper.OrderMapper;
import busness.ecommerce.repository.CartRepository;
import busness.ecommerce.repository.OrderRepository;
import busness.ecommerce.repository.UserRepository;

import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.List;

@Service
@RequiredArgsConstructor
@Transactional
public class OrderServiceImpl implements OrderService{

    private final CartRepository cartRepository;
    private final OrderRepository orderRepository;
    private final UserRepository userRepository;
    private final OrderMapper orderMapper;

    @Override
    public OrderResponseDto createOrder(Long userId) {
        User user = userRepository.findById(userId)
                .orElseThrow(() -> new RuntimeException("User not found"));

        Cart cart = cartRepository.findByUser(user)
                .orElseThrow(() -> new RuntimeException("Cart empty"));

        if (cart.getItems().isEmpty()) {
            throw new RuntimeException("Cart is empty");
        }

        Order order = Order.builder()
                .user(user)
                .status(OrderStatus.CREATED)
                .createdAt(LocalDateTime.now())
                .total(cart.getTotal())
                .build();

        List<OrderItem> items = cart.getItems()
                .stream()
                .map(ci -> OrderItem.builder()
                        .order(order)
                        .productVariant(ci.getProductVariant())
                        .price(ci.getPrice())
                        .sku(ci.getProductVariant().getSku())
                        .quantity(ci.getQuantity())
                        .seller(ci.getProductVariant().getProduct().getOwner())
                        .build())
                .toList();

        order.setItems(items);

        // sauvegarde commande
        Order savedOrder = orderRepository.save(order);

        // vider panier
        //cart.getItems().clear();
        //cart.setTotal(0.0);

        return orderMapper.toDto(savedOrder);
    }

    @Override
    public OrderResponseDto getOrderById(Long id) {
        Order order = orderRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Category not found"));
        return orderMapper.toDto(order);
    }

    @Override
    public List<OrderResponseDto> getAllOrders() {
        return orderRepository.findAll()
                .stream()
                .map(orderMapper::toDto)
                .toList();
    }

    @Override
    public List<OrderResponseDto> getOrdersByUser(Long userId) {
        User user = userRepository.findById(userId)
                .orElseThrow(() -> new RuntimeException("User not found"));

        return orderRepository.findByUser(user)
                .stream()
                .map(orderMapper::toDto)
                .toList();
    }

    @Override
    public List<OrdersByYearDto> getOrdersByYear() {
        return orderRepository.countOrdersByYear()
                .stream()
                .map(obj -> new OrdersByYearDto(
                        (Integer) obj[0],
                        (Long) obj[1]
                ))
                .toList();
    }

    @Override
    public List<OrdersByMonthDto> getOrdersByMonth(int year) {
        return orderRepository.countOrdersByMonth(year)
                .stream()
                .map(obj -> new OrdersByMonthDto(
                        (Integer) obj[0],
                        (Long) obj[1]
                ))
                .toList();
    }

    @Override
    public Long getCountCurrentMonthOrder(OrderStatus status) {
        LocalDateTime now = LocalDateTime.now();

        int month = now.getMonthValue();
        int year = now.getYear();
        return orderRepository.countOrderByStatusAndMonth(
                status,
                month,
                year

        );
    }

    @Override
    public List<OrderResponseDto> getOrdersCurrentMonthOrder(OrderStatus status) {
        LocalDateTime now = LocalDateTime.now();

        int month = now.getMonthValue();
        int year = now.getYear();
        return orderRepository.ordersByStatusAndMonth(status, month, year)
                .stream()
                .map(orderMapper::toDto)
                .toList();
    }
}
