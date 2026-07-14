package busness.ecommerce.services;

import busness.ecommerce.entity.Order;
import busness.ecommerce.enums.OrderStatus;
import busness.ecommerce.repository.OrderRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.List;

@Service
public class OrderSchedulerServiceImpl implements OrderSchedulerService{
    @Autowired
    private OrderRepository orderRepository;

    @Scheduled(fixedRate = 600000) // toutes les 10 minutes
    @Override
    public void cancelExpiredOrders() {
        List<Order> orders = orderRepository
                .findByStatusAndCreatedAtBefore(
                        OrderStatus.CREATED,
                        LocalDateTime.now().minusMinutes(30)
                );

        for(Order order : orders){
            order.setStatus(OrderStatus.CANCELED);
        }

        orderRepository.saveAll(orders);
    }
}
