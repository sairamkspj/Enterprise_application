import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms'; 
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-dashboard-comp',
  imports: [FormsModule,CommonModule],
  templateUrl: './dashboard-comp.html',
  styleUrl: './dashboard-comp.css'
})
export class DashboardComp {

  showOutOfStock = true;
  gridView = true;
  
  searchText = '';

    products = [
    { name: 'Laptop', price: 75000, stock: 5, discount: true },
    { name: 'Phone', price: 25000, stock: 0, discount: false },
    { name: 'Headphones', price: 2000, stock: 12, discount: false },
    { name: 'Shoes', price: 3000, stock: 0, discount: true }
  ];


  get filteredProducts() {
  if (this.showOutOfStock) {
    return this.products;
  }
  return this.products.filter(p => p.stock > 0);
}
}

