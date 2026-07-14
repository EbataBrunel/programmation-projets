package busness.ecommerce.controller;

import busness.ecommerce.config.StripeProperties;
import busness.ecommerce.dto.PaymentResponseDto;
import busness.ecommerce.services.PaymentService;
import com.stripe.model.Event;
import com.stripe.net.Webhook;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;

@RestController
@RequestMapping("/webhook")
@RequiredArgsConstructor
public class StripeWebhookController {

    private final PaymentService paymentService;
    private final StripeProperties stripeProperties;

    @PostMapping("/stripe")
    public ResponseEntity<String> handleStripeEvent(
            @RequestBody String payload,
            @RequestHeader("Stripe-Signature") String sigHeader
    ) {
        System.out.println("🔥 WEBHOOK RECU !");

        try {
            Event event = Webhook.constructEvent(
                    payload,
                    sigHeader,
                    stripeProperties.getWebhookSecret()
            );

            System.out.println("EVENT TYPE: " + event.getType());

            if ("checkout.session.completed".equals(event.getType())) {

                // 🔥 1. Parser le JSON brut
                JsonObject json = JsonParser.parseString(payload).getAsJsonObject();
                JsonObject data = json.getAsJsonObject("data");
                JsonObject object = data.getAsJsonObject("object");

                // 🔥 2. Récupérer metadata
                JsonObject metadata = object.getAsJsonObject("metadata");
                if (metadata == null) throw new RuntimeException("Metadata is null");

                String paymentIdStr = metadata.get("paymentId").getAsString();
                System.out.println("PAYMENT ID = " + paymentIdStr);
                Long paymentId = Long.valueOf(paymentIdStr);

                // 🔥 3. Vérification du montant
                Double amountStripe = object.get("amount_total").getAsDouble() / 100.0; // centimes → euros
                PaymentResponseDto payment = paymentService.getPaymentById(paymentId);

                if (Math.abs(amountStripe - payment.getAmount()) > 0.001) {
                    throw new RuntimeException("Montant incorrect !");
                }

                // 🔥 4. Mise à jour
                paymentService.handlePaymentSucceeded(paymentId);
                System.out.println("PAYMENT SUCCESFULLY UPDATED");
            }

            return ResponseEntity.ok("");

        } catch (Exception e) {
            e.printStackTrace();
            return ResponseEntity.status(400).body("Webhook error: " + e.getMessage());
        }
    }
}
