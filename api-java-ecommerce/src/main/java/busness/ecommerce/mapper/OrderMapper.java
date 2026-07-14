package busness.ecommerce.mapper;

import busness.ecommerce.dto.OrderItemResponseDto;
import busness.ecommerce.dto.OrderResponseDto;
import busness.ecommerce.entity.Order;
import org.springframework.stereotype.Component;

import java.util.List;

@Component
public class OrderMapper {

    public OrderResponseDto toDto(Order order) {

        List<OrderItemResponseDto> items = order.getItems()
                .stream()
                .map(i -> OrderItemResponseDto.builder()
                        .productVariationId(i.getProductVariant().getId())
                        .productName(i.getProductVariant().getProduct().getName())
                        .sku(i.getProductVariant().getSku())
                        .price(i.getPrice())
                        .quantity(i.getQuantity())
                        .subtotal(i.getPrice() * i.getQuantity())
                        .source(i.getProductSource())
                        .sellerId(i.getSeller().getId())
                        .sellerUsername(i.getSeller().getUsername())
                        .build())
                .toList();

        return OrderResponseDto.builder()
                .id(order.getId())
                .total(order.getTotal())
                .status(order.getStatus().name())
                .createdAt(order.getCreatedAt())
                .items(items)
                .build();
    }
}

