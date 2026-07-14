package busness.ecommerce.services;

import busness.ecommerce.dto.OrderItemResponseDto;
import busness.ecommerce.dto.OrderResponseDto;
import busness.ecommerce.dto.OrdersByMonthDto;
import busness.ecommerce.dto.OrdersByYearDto;
import busness.ecommerce.enums.OrderStatus;

import java.util.List;

public interface OrderService {
    OrderResponseDto createOrder(Long userId);

    OrderResponseDto getOrderById(Long id);

    List<OrderResponseDto> getAllOrders();

    List<OrderResponseDto> getOrdersByUser(Long userId);

    List<OrdersByYearDto> getOrdersByYear();

    List<OrdersByMonthDto> getOrdersByMonth(int year);

    Long getCountCurrentMonthOrder(OrderStatus status);

    List<OrderResponseDto> getOrdersCurrentMonthOrder(OrderStatus status);
}
