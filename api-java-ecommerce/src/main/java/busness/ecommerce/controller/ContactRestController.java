package busness.ecommerce.controller;

import busness.ecommerce.dto.*;
import busness.ecommerce.entity.Contact;
import busness.ecommerce.enums.OrderStatus;
import busness.ecommerce.services.ContactService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@CrossOrigin(origins = "http://localhost:4200")
@RestController
@RequestMapping("/api/v1/contacts")
@RequiredArgsConstructor
public class ContactRestController {
    private final ContactService contactService;

    // Ajouter un like
    @PostMapping
    public ResponseEntity<ContactResponseDto> create(
            @RequestBody ContactRequestDto dto
    ){
        return ResponseEntity.ok(contactService.createContact(dto));
    }

    @GetMapping("/grouped")
    public ResponseEntity<List<ContactGroupByDateDto>> getGroupedContacts() {
        return ResponseEntity.ok(contactService.getContactsGroupedByDate());
    }

    @GetMapping("/contact/{id}")
    public ResponseEntity<ContactResponseDto> getContact(
            @PathVariable Long id
    ) {
        return ResponseEntity.ok(contactService.getContact(id));
    }

    // Récupérer toutes les contacts
    @GetMapping
    public ResponseEntity<List<ContactResponseDto>> getAll() {
        return ResponseEntity.ok(contactService.getAllContacts());
    }

    @PatchMapping("/{id}/update-status")
    public ResponseEntity<ContactResponseDto> updateContactStatus(
            @PathVariable Long id,
            @RequestBody UpdateContactStatusRequestDto dto) {

        ContactResponseDto updatedContact = contactService.updateContact(id, dto);
        return ResponseEntity.ok(updatedContact);
    }

    @PatchMapping("/status/update-all")
    public ResponseEntity<Integer> updateAllContactsStatus() {
        int updatedCount = contactService.updateAllContactsStatus();
        return ResponseEntity.ok(updatedCount);
    }

    @GetMapping("/count/status/{status}")
    public ResponseEntity<Integer> getCountContactStatus(
            @PathVariable Integer status
    ) {
        return ResponseEntity.ok(contactService.getCountContactStatus(status));
    }

    // Supprimer un like
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(
            @PathVariable Long id
    ) {
        contactService.deleteContact(id);
        return ResponseEntity.noContent().build();
    }
}
