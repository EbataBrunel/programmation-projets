package eajc.group.apv.controller;

import eajc.group.apv.dto.*;
import eajc.group.apv.entity.Contact;
import eajc.group.apv.services.ContactService;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/api/v1/contacts")
public class ContactRestController {
    private final ContactService contactService;

    public ContactRestController(ContactService contactService) {
        this.contactService = contactService;
    }

    // Ajouter un like
    @PostMapping
    public ResponseEntity<ContactResponseDto> create(
            @RequestBody ContactRequestDto dto
    ){
        return ResponseEntity.ok(contactService.createContact(dto));
    }

    @PreAuthorize("hasAnyRole('ADMIN', 'SUPADMIN')")
    @GetMapping("/grouped")
    public ResponseEntity<List<ContactGroupByDateDto>> getGroupedContacts() {
        return ResponseEntity.ok(contactService.getContactsGroupedByDate());
    }

    @PreAuthorize("hasAnyRole('ADMIN', 'SUPADMIN')")
    @GetMapping("/contact/{publicId}")
    public ResponseEntity<ContactResponseDto> getContact(
            @PathVariable UUID publicId
            ) {
        return ResponseEntity.ok(contactService.getContact(publicId));
    }

    @PreAuthorize("hasAnyRole('ADMIN', 'SUPADMIN')")
    // Récupérer toutes les contacts
    @GetMapping
    public ResponseEntity<List<ContactResponseDto>> getAll() {
        return ResponseEntity.ok(contactService.getAllContacts());
    }

    @PreAuthorize("hasAnyRole('ADMIN', 'SUPADMIN')")
    @PatchMapping("/{publicId}/update-status")
    public ResponseEntity<ContactResponseDto> updateContactStatus(
            @PathVariable UUID publicId,
            @RequestBody UpdateContactStatusRequestDto dto) {

        ContactResponseDto updatedContact = contactService.updateContact(publicId, dto);
        return ResponseEntity.ok(updatedContact);
    }

    @PreAuthorize("hasAnyRole('ADMIN', 'SUPADMIN')")
    @PatchMapping("/status/update-all")
    public ResponseEntity<Integer> updateAllContactsStatus() {
        int updatedCount = contactService.updateAllContactsStatus();
        return ResponseEntity.ok(updatedCount);
    }

    @PreAuthorize("hasAnyRole('ADMIN', 'SUPADMIN')")
    @GetMapping("/count/status/{status}")
    public ResponseEntity<Integer> getCountContactStatus(
            @PathVariable Integer status
    ) {
        return ResponseEntity.ok(contactService.getCountContactStatus(status));
    }

    @PreAuthorize("hasAnyRole('ADMIN', 'SUPADMIN')")
    // Supprimer un like
    @DeleteMapping("/{publicId}")
    public ResponseEntity<Void> delete(
            @PathVariable UUID publicId
    ) {
        contactService.deleteContact(publicId);
        return ResponseEntity.noContent().build();
    }
}
