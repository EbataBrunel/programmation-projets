package busness.ecommerce.controller;

import busness.ecommerce.dto.CategoryResponseDto;
import busness.ecommerce.dto.OrderResponseDto;
import busness.ecommerce.dto.OrdersByMonthDto;
import busness.ecommerce.dto.OrdersByYearDto;
import busness.ecommerce.enums.OrderStatus;
import busness.ecommerce.services.OrderService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@CrossOrigin(origins = "http://localhost:4200")
@RestController
@RequestMapping(value = "/api/v1/orders")
@RequiredArgsConstructor
public class OrderRestController {
    private final OrderService orderService;

    // liste des commandes

    @GetMapping
    public ResponseEntity<List<OrderResponseDto>> getAllOrders(){
        return ResponseEntity.ok(orderService.getAllOrders());
    }

    // Récupérer une commande par id
    @GetMapping("/{id}")
    public ResponseEntity<OrderResponseDto> getOne(
            @PathVariable Long id
    ) {
        return ResponseEntity.ok(orderService.getOrderById(id));
    }

    // créer une commande
    @PostMapping("/user/{userId}")
    public ResponseEntity<OrderResponseDto> createOrder(
            @PathVariable Long userId
    ) {
        return ResponseEntity.ok(orderService.createOrder(userId));
    }

    // liste des commandes du user
    @GetMapping("/user/{userId}")
    public ResponseEntity<List<OrderResponseDto>> getOrders(
            @PathVariable Long userId
    ) {
        return ResponseEntity.ok(orderService.getOrdersByUser(userId));
    }

    // Liste des commandes par année
    @GetMapping("/stats/years")
    public List<OrdersByYearDto> ordersByYear() {
        return orderService.getOrdersByYear();
    }

    // Lise des commandes d'une année
    @GetMapping("/stats/months/{year}")
    public List<OrdersByMonthDto> ordersByMonth(@PathVariable int year) {
        return orderService.getOrdersByMonth(year);
    }

    @GetMapping("/count/month/{status}")
    public ResponseEntity<Long> getCountOrdersCurrentMonth(
            @PathVariable OrderStatus status
            ) {
        return ResponseEntity.ok(orderService.getCountCurrentMonthOrder(status));
    }

    @GetMapping("/month/{status}")
    public ResponseEntity<List<OrderResponseDto>> getOrdersCurrentMonth(
            @PathVariable OrderStatus status
    ) {
        return ResponseEntity.ok(orderService.getOrdersCurrentMonthOrder(status));
    }
}
